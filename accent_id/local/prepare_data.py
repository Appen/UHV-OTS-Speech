#!/usr/bin/env python3
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("wav_dir", type=str,help="directory to wav file")
parser.add_argument("data_dir", type=str,help="data directory")

args = parser.parse_args()

wav_dir=args.wav_dir
data_dir=args.data_dir

os.system('mkdir -p ' + data_dir)
lang = wav_dir.split('/')[-1]

f_wav = open(data_dir+'/wav.scp', 'a')
f_utt2spk = open(data_dir+'/utt2spk', 'a')
f_utt2dur = open(data_dir+'/utt2dur', 'a')
f_utt2lang = open(data_dir+'/utt2lang', 'a')

wav_files=os.listdir(wav_dir)
for f in wav_files:
    ID = f[0:-4]
    spk = ID.split('---')[0]
    time = ID.split('---')[1]
    time_st = float(time.split('-')[0])
    time_ed = float(time.split('-')[1])
    dur = time_ed - time_st
    if dur >= 5.0:
        f_wav.write(ID + '\t' + wav_dir + '/'+ f + '\n')
        f_utt2spk.write(ID + '\t' + spk + '\n')
        f_utt2dur.write(ID + '\t' + str(dur) + '\n')
        f_utt2lang.write(ID + '\t' + lang + '\n')





