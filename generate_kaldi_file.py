import os 
import sys
import json
import glob

batch_folder = sys.argv[1]

utt_wavs = glob.glob(batch_folder+'/audio-utterance/*/*.wav')
spkr_jsons =glob.glob(batch_folder+'/batch_spkr_info/*.json')


wav_scp = []
text = []
utt2spk = []
spk2gender =set()


for utt_wav_f in utt_wavs:
    print(utt_wav_f)
    utt_wav_json = utt_wav_f.split('.wav')[0]+'.json'
        
    f = open(utt_wav_json)
    data = json.load(f)
    f.close()
    
    spkr = data['speaker_id']
    utt_id = spkr+'-'+data['utterance_id']
    session_id = data['session_id']
    gender = data['gender'][0]

    spkr_id = spkr
    trans = data['transcription']

    wav_scp.append(utt_id+' '+utt_wav_f)
    text.append(utt_id+' '+trans)
    utt2spk.append(utt_id+' '+spkr_id)
    if gender in ['f', 'm']:
        spk2gender.add(spkr_id+' '+gender)

with open(batch_folder+'./wav.scp','w') as fid:
    for ln in sorted(wav_scp):
        print(ln)
        fid.write(ln+'\n')

with open(batch_folder+'./text','w') as fid:
    for ln in sorted(text):
        print(ln)
        fid.write(ln+'\n')


with open(batch_folder+'./utt2spk','w') as fid:
    for ln in sorted(utt2spk):
        print(ln)
        fid.write(ln+'\n')

with open (batch_folder+'./spk2gender','w') as fid:
    for ln in sorted(spk2gender):
        print(ln)
        fid.write(ln+'\n')

cmd_ln='/opt/kaldi/egs/librispeech/s5/utils/utt2spk_to_spk2utt.pl '+batch_folder+'./utt2spk > '+batch_folder+'./spk2utt'
os.popen(cmd_ln)

    
    




    


