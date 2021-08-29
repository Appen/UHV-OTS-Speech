#!/usr/bin/python3
"""
20210706:

---------------------------------------------------------

"""

import os
import sys
import pickle
import torch
import torchaudio
from tqdm.contrib import tqdm
import speechbrain as sb
import numpy
from hyperpyyaml import load_hyperpyyaml
from speechbrain.processing.PLDA_LDA import StatObject_SB
from speechbrain.utils.distributed import run_on_main

def compute_embeddings(wavs, wav_lens):
    """
    wavs: Tensor containing the speech waveform (batch, time). Make sure the sample rate is fs=16000 Hz.
    wav_lens: Tensor containing the relative length for each sentence in the length (e.g., [0.8 0.6 1.0])
    """
    print("  -----Start: compute_embeddings()-----")
    params_device = params["device"]
    print("  params_device = ", params_device)
    wavs = wavs.to(params_device)
    wav_lens = wav_lens.to(params_device)
    with torch.no_grad():
        params_compute_features = params["compute_features"]
        params_mean_var_norm = params["mean_var_norm"]
        params_embedding_model = params["embedding_model"]
        params_mean_var_norm_emb = params["mean_var_norm_emb"]
        #print("  params_compute_features = ", params_compute_features)
        print("  params_mean_var_norm = ", params_mean_var_norm)
        #print("  params_embedding_model = ", params_embedding_model)
        print("  params_mean_var_norm_emb = ", params_mean_var_norm_emb)
        
        params_compute_features.to(params_device)
        params_mean_var_norm.to(params_device)
        params_embedding_model.to(params_device)
        params_mean_var_norm_emb.to(params_device)
        
        feats = params_compute_features(wavs)
        #print("  feats = \n", feats)
        #feats_np = feats.cpu().detach().numpy()
        #print(" feats_sum = ", numpy.sum(feats_np))
        #print("feas_nan_check:", torch.isnan(feats))
        #print("  feats.shape = ", feats.shape)
        feats = params_mean_var_norm(feats, wav_lens)
        embeddings = params_embedding_model(feats, wav_lens)
        #print("  embeddings = \n", embeddings)
        #print("  embeddings.shape = ", embeddings.shape)
        #embeddings_np = embeddings.cpu().detach().numpy()
        #print("  embeddings_sum = ", numpy.sum(embeddings_np))
        #np_isnan_arr = numpy.isnan(embeddings_np)
        #print("  np_isnan_arr = ", np_isnan_arr)
        #nan_cnt = (np_isnan_arr==True).sum()
        #print("  nan_cnt = ", nan_cnt)
        #nan_index = numpy.where(np_isnan_arr==True)
        #print("  nan_index = \n", nan_index)
        embeddings = params_mean_var_norm_emb(embeddings, torch.ones(embeddings.shape[0]).to(embeddings.device)) 
        #print("  embeddings = \n", embeddings)
        #embeddings_np = embeddings.cpu().detach().numpy()
        #print("  embeddings_sum = ", numpy.sum(embeddings_np))
        #print("  embeddings.shape = ", embeddings.shape)
    print("  -----End: compute_embeddings()-----")
    return embeddings.squeeze(1)


def dataio_prep(params):
    print("  -----Start: dataio_prep()-----")
    data_folder = params["data_folder"]
    params_train_data = params["train_data"]
    params_n_train_snts = params["n_train_snts"]
    params_enrol_data = params["enrol_data"]
    params_test_data = params["test_data"]
    print("  data_folder = ", data_folder)
    print("  params_train_data = ", params_train_data)
    print("  params_n_train_snts = ", params_n_train_snts)
    print("  params_enrol_data = ", params_enrol_data)
    print("  params_test_data = ", params_test_data)

    #train_data = sb.dataio.dataset.DynamicItemDataset.from_csv(
    #    csv_path=params_train_data, replacements={"data_root": data_folder},)
    #train_data = train_data.filtered_sorted(
    #    sort_key="duration", select_n=params_n_train_snts)
    #print("  train_data = ", train_data)

    enrol_data = sb.dataio.dataset.DynamicItemDataset.from_csv(
        csv_path=params_enrol_data, replacements={"data_root": data_folder},)
    enrol_data = enrol_data.filtered_sorted(sort_key="duration")
    print("  enrol_data = ", enrol_data)

    test_data = sb.dataio.dataset.DynamicItemDataset.from_csv(
        csv_path=params_test_data, replacements={"data_root": data_folder},)
    test_data = test_data.filtered_sorted(sort_key="duration")
    print("  test_data = ", test_data)

    #datasets = [train_data, enrol_data, test_data]
    datasets = [enrol_data, test_data]
    #print("  datasets = ", datasets)

    # Define audio pipeline:
    @sb.utils.data_pipeline.takes("wav", "start", "stop")
    @sb.utils.data_pipeline.provides("sig")
    def audio_pipeline(wav, start, stop):
        start = int(start)
        stop = int(stop)
        num_frames = stop - start
        sig, fs = torchaudio.load(wav, num_frames=num_frames, frame_offset=start)
        sig = sig.transpose(0, 1).squeeze(1)
        return sig
    sb.dataio.dataset.add_dynamic_item(datasets, audio_pipeline)

    # Set output:
    sb.dataio.dataset.set_output_keys(datasets, ["id", "sig", "spk_id"])

    #params_train_dataloader_opts = params["train_dataloader_opts"]
    params_enrol_dataloader_opts = params["enrol_dataloader_opts"]
    params_test_dataloader_opts = params["test_dataloader_opts"]
    #print("  params_train_dataloader_opts = ", params_train_dataloader_opts)
    print("  params_enrol_dataloader_opts = ", params_enrol_dataloader_opts)
    print("  params_test_dataloader_opts = ", params_test_dataloader_opts)

    #train_dataloader = sb.dataio.dataloader.make_dataloader(train_data, **params_train_dataloader_opts)
    enrol_dataloader = sb.dataio.dataloader.make_dataloader(enrol_data, **params_enrol_dataloader_opts)
    test_dataloader = sb.dataio.dataloader.make_dataloader(test_data, **params_test_dataloader_opts)
    #print("  train_dataloader = ", train_dataloader)
    print("  enrol_dataloader = ", enrol_dataloader)
    print("  test_dataloader = ", test_dataloader)
    print("  -----End: dataio_prep()-----")
    #return train_dataloader, enrol_dataloader, test_dataloader
    return enrol_dataloader, test_dataloader


if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    print("  current_dir = ", current_dir)
    sys.path.append(os.path.dirname(current_dir))

    all_parameters = sys.argv[1:]
    print("  all_parameters = \n", all_parameters)
    params_file, run_opts, overrides = sb.core.parse_arguments(all_parameters)
    print("  params_file = ", params_file)
    print("  run_opts = ", run_opts)
    print("  overrides = ", overrides)
    with open(params_file) as fin: params = load_hyperpyyaml(fin, overrides)
    #print("  params = ", params)
    

    params_data_folder = params["data_folder"]
    params_save_folder = params["save_folder"]
    params_verification_file = params["verification_file"]
    veri_file_path = os.path.join(params_save_folder, os.path.basename(params_verification_file))
    print("  params_data_folder = ", params_data_folder)
    print("  params_save_folder = ", params_save_folder)
    print("  params_verification_file = ", params_verification_file)
    print("  veri_file_path = ", veri_file_path)

    '''
    params_output_folder = params["output_folder"]
    print("  params_output_folder = ", params_output_folder)
    sb.core.create_experiment_directory(experiment_directory=params_output_folder, 
                                        hyperparams_to_save=params_file,
                                        overrides=overrides,)
    '''

    
    # here we create the datasets objects as well as tokenization and encoding
    #train_dataloader, enrol_dataloader, test_dataloader = dataio_prep(params)
    enrol_dataloader, test_dataloader = dataio_prep(params)
    modelset, segset = [], []
    embeddings = numpy.empty(shape=[0, params["emb_dim"]], dtype=numpy.float64)
    print("  embeddings = ", embeddings)
    print("  embeddings.shape = ", embeddings.shape, ", type(embeddings) = ", type(embeddings))

    # Embedding file for train data
     
    #xv_file_prefix = params["train_data"].split('/')[-1].split('.')[0]
    #print("  xv_file_prefix = ", xv_file_prefix)
    #embedding_obj_name = "embedding_obj_" + xv_file_prefix + ".pkl"
    #xv_file = os.path.join(params_save_folder, embedding_obj_name)
    #xv_file = os.path.join(params_save_folder, "voxceleb1_ots_asr001_asr003_voxceleb2_train_embeddings_stat_obj.pkl")
    #xv_file = os.path.join(params_save_folder, "voxceleb1_train_embeddings_stat_obj.pkl")
    #xv_file = os.path.join(params_save_folder, "voxceleb1_train_1000_embeddings_stat_obj.pkl")
    #xv_file = os.path.join(params_save_folder, "voxceleb1_test_200_embeddings_stat_obj.pkl")
    #print("  xv_file = ", xv_file)

    params_device = params["device"]
    params_embedding_model = params["embedding_model"]
    print("  params_device = ", params_device)
    #print("  params_embedding_model = ", params_embedding_model)

    # Download the pretrained LM from HuggingFace
    params_pretrainer = params["pretrainer"]
    print("  params_pretrainer = ", params_pretrainer)

    run_on_main(params_pretrainer.collect_files)
    #params_pretrainer.load_collected()
    params_pretrainer.load_collected(device=params_device)

    params_embedding_model.eval()
    params_embedding_model.to(params_device)

    # Computing training embeddings (skip it of if already extracted)
    '''
    print("Extracting embeddings from Training set..")
    with tqdm(train_dataloader, dynamic_ncols=True) as t:
        print("  t = ", t)
        for batch in t:
            print("=============================================")
            print("    batch = ", batch)
            snt_id = batch.id
            wav, lens = batch.sig
            spk_ids = batch.spk_id
            print("    snt_id = ", snt_id)
            print("    len(snt_id) = ", len(snt_id))
            #print("    wav = ", wav)
            print("    wav.shape = ", wav.shape)
            print("    lens = \n", lens)
            print("    lens.shape = ", lens.shape)
            print("    spk_ids = ", spk_ids)
            print("    len(spk_ids) = ", len(spk_ids))

            # Flattening speaker ids
            modelset = modelset + spk_ids
	    # For segset
            segset = segset + snt_id

            # Compute embeddings
            emb = compute_embeddings(wav, lens)
            xv = emb.squeeze(1).cpu().numpy()
            embeddings = numpy.concatenate((embeddings, xv), axis=0)
            #print("     emb = \n", emb)
            print("     emb.shape = ", emb.shape)
            print("     xv = \n", xv)
            print("     xv.shape = ", xv.shape)
            #print("     embeddings = \n", embeddings)
            print("     embeddings.shape = ", embeddings.shape)
    '''
    # Speaker IDs and utterance IDs
    modelset = numpy.array(modelset, dtype="|O")
    segset = numpy.array(segset, dtype="|O")
    print("modelset = \n", modelset)
    print("segset = \n", segset)

    # Intialize variables for start, stop and stat0
    s = numpy.array([None] * embeddings.shape[0])
    b = numpy.array([[1.0]] * embeddings.shape[0])
    print("  s = ", s)
    print("  s.shape = ", s.shape, ", type(s) = ", type(s))
    print("  b = \n", b)
    print("  b.shape = ", b.shape, ", type(b) = ", type(b))

    embeddings_stat = StatObject_SB(modelset=modelset, segset=segset, start=s, stop=s, stat0=b, stat1=embeddings,)
    del embeddings

    # Save TRAINING embeddings in StatObject_SB object
    #embeddings_stat.save_stat_object(xv_file)
    #print("  $$$ generate x-vector file: ", xv_file)
