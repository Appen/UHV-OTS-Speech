#!/usr/bin/env python3
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("wav_dir", type=str,help="directory to wav file")
parser.add_argument("data_dir", type=str,help="data directory")

args = parser.parse_args()

wav_dir=args.wav_dir + '/wav'
data_dir=args.data_dir

os.system('mkdir -p ' + data_dir)
lang = 'uk'

f_wav = open(data_dir+'/wav.scp', 'a')
f_utt2spk = open(data_dir+'/utt2spk', 'a')
f_utt2dur = open(data_dir+'/utt2dur', 'a')
f_utt2lang = open(data_dir+'/utt2lang', 'a')



