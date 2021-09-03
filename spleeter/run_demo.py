#!/usr/bin/python3

import os,sys
import glob
os.chdir('/opt/spleeter')

from spleeter.separator import Separator

#import Separator
# Using embedded configuration.
separator = Separator('spleeter:2stems')

input_dir = /opt/scripts/source_separation/sample_audio #sys.argv[1]
output_dir = /opt/scripts/source_separation/output #sys.argv[2]


all_wav = glob.glob(input_dir+"*.wav")
if len(all_wav) ==0:
    print('No wav files in '+input_dir)
    exit()

for wav_f in all_wav:
    fileid = os.path.basename(wav_f).split('.wav')[0]
    os.mkdir(output_dir+'/'+fileid)
    separator.separate_to_file(wav_f, output_dir+'/'+fileid)    

