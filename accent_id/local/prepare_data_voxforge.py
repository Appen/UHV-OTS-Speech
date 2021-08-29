#!/usr/bin/env python3
import os
import argparse
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("wav_dir", type=str,help="directory to wav file")
parser.add_argument("langID", type=str,help="lanugae ID, uk or us")
parser.add_argument("data_dir", type=str,help="data directory")

args = parser.parse_args()
wav_dir= args.wav_dir
langID = args.langID
data_dir= args.data_dir

f_wav = open(data_dir+'/wav.scp', 'a')
f_utt2spk = open(data_dir+'/utt2spk', 'a')
f_utt2dur = open(data_dir+'/utt2dur', 'a')
f_utt2lang = open(data_dir+'/utt2lang', 'a')

sub_dir = os.listdir(wav_dir)
for d in sub_dir:
    spk = d.split('-')[0]
    if os.path.isdir(wav_dir + '/' + d + '/wav'):
        file_dir = wav_dir + '/' + d + '/wav' 
        files = os.listdir(file_dir)
        for f in files:
            ID = d + '-' + f[0:-4]
            duration = subprocess.check_output("soxi -D " + file_dir + '/' + f, shell=True)
            duration = duration.decode('utf8').strip()

            if float(duration) >= 5:
                f_wav.write(ID + '\t' + file_dir + '/'+ f + '\n')
                f_utt2spk.write(ID + '\t' + spk + '\n')
                f_utt2dur.write(ID + '\t' + str(duration) + '\n') 
                f_utt2lang.write(ID + '\t' + langID + '\n') 

    elif os.path.isdir(wav_dir + '/' + d + '/flac'):
        file_dir = wav_dir + '/' + d + '/flac'
        files = os.listdir(file_dir)
        for f in files:
            ID = d + '-' + f[0:-5]
            duration = subprocess.check_output("soxi -D " + file_dir + '/' + f, shell=True)
            duration = duration.decode('utf8').strip()

            if float(duration) >= 5:
                f_wav.write(ID + '\t' + 'flac -c -d -s ' + file_dir + '/'+ f + '\n')
                f_utt2spk.write(ID + '\t' + spk + '\n')
                f_utt2dur.write(ID + '\t' + str(duration) + '\n')
                f_utt2lang.write(ID + '\t' + langID + '\n')    








