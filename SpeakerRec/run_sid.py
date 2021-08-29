#!/usr/bin/python3

import os
import sys
import csv
import torch
import logging
import torchaudio
import speechbrain as sb
from tqdm.contrib import tqdm
from hyperpyyaml import load_hyperpyyaml
from speechbrain.utils.metric_stats import EER, minDCF
from speechbrain.utils.data_utils import download_file
from speechbrain.utils.distributed import run_on_main

SAMPLERATE = 16000

def prepare_trial(enrol_spk, test_file):
    ft = open(test_file, 'r')
    fo = open('results/voxceleb1_2/speaker_verification_ecapa_big/save/trials.txt', 'w')
    for line in ft.readlines():
        wav = line.split()[0]
        spk = wav.split('/')[-3]
        for es in enrol_spk:
            if spk == es:
                real = 1
            else:
                real = 0
            print_line = str(real) + ' ' + es + ' ' + wav + '\n'
            fo.write(print_line)
    ft.close()
    fo.close()

def select_spk(spk_id):
    spk = 'id10270'
    if spk_id == spk:
        return True
    else:
        return False

def dataio_prep(params):
    data_folder = params["data_folder"]
    test_data = sb.dataio.dataset.DynamicItemDataset.from_csv(
        csv_path=params["test_data"], replacements={"data_root": data_folder},
    )
    test_data = test_data.filtered_sorted(sort_key="duration")
    datasets = [test_data]

    #test_data1 = test_data.filtered_sorted(key_test={'spk_id': select_spk}) 

    @sb.utils.data_pipeline.takes("wav", "start", "stop")
    @sb.utils.data_pipeline.provides("sig")
    def audio_pipeline(wav, start, stop):
        start = int(start)
        stop = int(stop)
        num_frames = stop - start
        sig, fs = torchaudio.load(
           wav, num_frames=num_frames, frame_offset=start
        )
        sig = sig.transpose(0, 1).squeeze(1)
        return sig

    sb.dataio.dataset.add_dynamic_item(datasets, audio_pipeline)
    sb.dataio.dataset.set_output_keys(datasets, ["id", "sig"])

    test_dataloader = sb.dataio.dataloader.make_dataloader(
        test_data, **params["test_dataloader_opts"]
    )

    return test_dataloader

def compute_embedding(wavs, wav_lens):
    with torch.no_grad():
        feats = params["compute_features"](wavs)
        feats = params["mean_var_norm"](feats, wav_lens)
        embeddings = params["embedding_model"](feats, wav_lens)
        embeddings = params["mean_var_norm_emb"](
            embeddings, torch.ones(embeddings.shape[0]).to(embeddings.device)
        )
    return embeddings.squeeze(1)





def compute_embedding_loop(data_loader):
    embedding_dict = {}
    with torch.no_grad():
        for batch in tqdm(data_loader, dynamic_ncols=True):
            batch = batch.to(params["device"])
            seg_ids = batch.id
            wavs, lens = batch.sig
            found = False
            for seg_id in seg_ids:
                if seg_id not in embedding_dict:
                    found = True
                if not found:
                    continue
                wavs, lens = wavs.to(params["device"]), lens.to(params["device"])
                emb = compute_embedding(wavs, lens).unsqueeze(1)
                for i, seg_id in enumerate(seg_ids):
                    embedding_dict[seg_id] = emb[i].detach().clone()
  
    return embedding_dict



def get_verification_scores(veri_test):
    scores = []
    positive_scores = []
    negative_scores = []

    save_file = os.path.join(params["output_folder"], "scores.txt")
    s_file = open(save_file, "w")

    similarity = torch.nn.CosineSimilarity(dim=-1, eps=1e-6)

    for i, line in enumerate(veri_test):
        lab_pair = int(line.split(" ")[0].rstrip().split(".")[0].strip())
        enrol_id = line.split(" ")[1].rstrip().split(".")[0].strip()
        test_id = line.split(" ")[2].rstrip().split(".")[0].strip()
        enrol = enrol_spk_dict[enrol_id]
        test = test_dict[test_id]

        score = similarity(enrol, test)[0]
        s_file.write("%s %s %i %f\n" % (enrol_id, test_id, lab_pair, score))
        scores.append(score)
        if lab_pair == 1:
            positive_scores.append(score)
        else:
            negative_scores.append(score)
    s_file.close()
    return positive_scores, negative_scores

def add_utts_to_enrol(enrol_id, utts, threshold, data_folder):
# add utts to enrol list of existing speaker enrol_id    
    test_utt_keep = []
    xvector_enrol_id = enrol_spk_dict[enrol_id]
      
    for i in utts: # only  add test utts with high score
        test_id = i.split('.')[0]
        score = similarity(xvector_enrol_id, test_dict[test_id])[0]
        if score > threshold:
            test_utt_keep.append(i)
                    

    #enrol_utts = torch.load(enrol_spk2utts_file) #csv file may contain this info
    
    #for i in test_utts_keep:
    #    enrol_utts{enrol_id}.append(i)

    enrol_data = sb.dataio.dataset.DynamicItemDataset.from_csv(
        csv_path=params["enrol_data"], replacements={"data_root": data_folder},
    )
    enrol_data_4spk = enrol_data.filtered_sorted(key_test={'spk_id': select_spk}) 
    datasets = [enrol_data_4spk]
    @sb.utils.data_pipeline.takes("wav", "start", "stop")
    @sb.utils.data_pipeline.provides("sig")
    def audio_pipeline(wav, start, stop):
        start = int(start)
        stop = int(stop)
        num_frames = stop - start
        sig, fs = torchaudio.load(
        wav, num_frames=num_frames, frame_offset=start
        )
        sig = sig.transpose(0, 1).squeeze(1)
        return sig
    sb.dataio.dataset.add_dynamic_item(datasets, audio_pipeline)
    sb.dataio.dataset.set_output_keys(datasets, ["id", "sig"])

    enrol_4spk_dataloader = sb.dataio.dataloader.make_dataloader(
        enrol_data_4spk, **params["enrol_dataloader_opts"])
    enrol_4spk_dict = compute_embedding_loop(enrol_4spk_dataloader) # get embeddings of enrolled utts only for enrol_id

    for i in test_utt_keep:
        enrol_4spk_dict[i] = test_dict[i.split('.')[0]]
     
    embeddings_mean = sum(enrol_4spk_dict.values())/len(enrol_4spk_dict)
    enrol_spk_dict[enrol_id] = embeddings_mean # update enrol_dict
  
    added_entry = []
    for i in utts:
        utt_dir = params['data_folder'] 
        wav_file = i
        audio_id = i.split('.')[0]
        signal,fs = torchaudio.load(wav_file)
        signal = signal.squeeze(0)
        audio_duration = signal.shape[0] / SAMPLERATE
        start_sample = 0
        stop_sample = signal.shape[0]
     
        csv_line = [
            audio_id,
            str(audio_duration),
            wav_file,
            start_sample,
            stop_sample,
            enrol_id,
        ]
        added_entry.append(csv_line)
    csv_file = 'results/voxceleb1_2/speaker_verification_ecapa_big/save/enrol.csv'    
    with open(csv_file, mode="a") as csv_f:
        csv_writer = csv.writer(csv_f, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for line in added_entry:
            csv_writer.writerow(line)
    return enrol_spk_dict

def add_spk_to_enrol(utts, spk):
    #update enrol speaker embeddings
    embeddings = []
    for i in utts:
        embeddings.append(test_dict[utts])
    enrol_spk_dict[spk] = sum(embeddings)/len(embeddings)    
    
    #update csv file
    added_entry = []
    for i in utts:
        wav_file = i
        audio_id = i
        signal,fs = torchaudio.load(wav_file)
        signal = signal.squeeze(0)
        audio_duration = signal.shape[0] / SAMPLERATE
        start_sample = 0
        stop_sample = signal.shape[0]

        csv_line = [
            audio_id,
            str(audio_duration),
            wav_file,
            start_sample,
            stop_sample,
            spk_id,
        ]
        added_entry.append(csv_line)
    with open(csv_file, mode="a") as csv_f:    
        csv_writer = csv.writer(
                csv_f, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
        )
        for line in added_entry:
            csv_writer.writerow(line)

      #update speaker to utt info
    spk2utt[spk] = []
    for i in utt:
        spk2utt[spk].append(i)






                                                                                      


if __name__ == "__main__":    
    # Logger setup
    logger = logging.getLogger(__name__)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.dirname(current_dir))

    params_file, run_opts, overrides = sb.core.parse_arguments(sys.argv[1:])
    with open(params_file) as fin:
        params = load_hyperpyyaml(fin, overrides)
     
    
    model_file = 'results/voxceleb1_2/speaker_verification_ecapa_big/save/enrol_model.md'
    enrol_spk_dict = torch.load(model_file)
    enrol_spk = []
    for key in enrol_spk_dict.keys():  # existing speakers
        enrol_spk.append(key)
    test_file = 'results/voxceleb1_2/speaker_verification_ecapa_big/save/test_file.txt'
    prepare_trial(enrol_spk, test_file) 
    veri_file_path = 'results/voxceleb1_2/speaker_verification_ecapa_big/save/trials.txt'
    from prepare_ots import prepare_ots_test

    sb.core.create_experiment_directory(
        experiment_directory=params["output_folder"],
        hyperparams_to_save=params_file,
        overrides=overrides,
    )
    
    # make csv for test utters
    test_audio_folder = params['data_folder']
    prepare_ots_test(
        data_folder=test_audio_folder,
        save_folder=params["save_folder"],
        verification_pairs_file=veri_file_path,
        splits=["test"],
        seg_dur=300
    )

    test_dataloader = dataio_prep(params)

    run_on_main(params["pretrainer"].collect_files)
    params["pretrainer"].load_collected(params["device"])
    params["embedding_model"].eval()
    params["embedding_model"].to(params["device"])
     

    test_dict = compute_embedding_loop(test_dataloader)
    #itest_dict.to(embeddings.device)
    with open(veri_file_path) as f:
        veri_test = [line.rstrip() for line in f]
    positive_scores, negative_scores = get_verification_scores(veri_test)
    eer = EER(torch.tensor(positive_scores), torch.tensor(negative_scores))
    '''
    with open(test_file) as f:
        line = f.readline()
    session_id = line.split('/')[1]
    spk2utt = {}
    with open(test_file) as f:
        for line in f:
            spk = line.strip().split()[1]
            utt = line.strip().split()[0]
            if spk in spk2utt:
                spk2utt[spk].append(utt)
            else:
                spk2utt[spk] = []
                spk2utt[spk].append(utt)
    # Cosine similarity initialization
    similarity = torch.nn.CosineSimilarity(dim=-1, eps=1e-6)
    threshold = -0.5
    for spk in spk2utt.keys():
        spk2enrol = []
        utt_num = len(spk2utt[spk])
        spk_added = []
        for test in spk2utt[spk]:
            testID = test.split('.')[0]
            xvector_t = test_dict[testID]
            scores_for_one_spk = {}
            max_score = float('-inf')
            for enrol in enrol_spk_dict.keys():
                xvector_e = enrol_spk_dict[enrol]
                score = similarity(xvector_e, xvector_t)[0]
                if score > max_score:
                    max_score = score
                    ID = enrol
            if max_score > threshold:
                spk2enrol.append(ID)
        freq = {}
        utts2enrol = {}
        for i in spk2enrol:
            if i in freq:
                freq[i] += 1
                #utts2enrol[i].append()
            else:
                freq[i] = 1
        for i in freq:
            enrol_id = i
            percent = freq[i]/utt_num
            if percent > 0.8:
                enrol_spk_dict = add_utts_to_enrol(enrol_id, spk2utt[spk], threshold, params['data_folder'])
                spk_id = enrol_id
            else:
                spk_added.append()
                spk_added.append(spk_id)
                add_spk_to_enrol(spk2utt[spk], spk_id)
       
    #update threshold
    negative = []
    for spk in spk_added:
        for utt in spk2utt[spk]:
            testID = test.split('.')[0]
            xvector_t = test_dict[testID]
            for enrol in enrol_spk_dict.keys():
                if enrol != spk:
                    xvector_e = enrol_spk_dict[enrol]
                    negative.append(similarity(xvector_e, xvector_t)[0])
    thresholds = rotch.unique(negative)
    interm_thresholds = (thresholds[0:-1] + thresholds[1:]) / 2
    thresholds, _ = torch.sort(torch.cat([thresholds, interm_thresholds]))

    negative_scores = torch.cat(
                    len(thresholds) * [negative.unsqueeze(0)]
                        )
    neg_scores_threshold = negative_scores.transpose(0, 1) > thresholds
    FAR = (neg_scores_threshold.sum(0)).float() / negative_scores.shape[1]
    '''




                



