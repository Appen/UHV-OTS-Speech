#!/usr/bin/env python3
import os

wav_file='exp/xvect_eval_short/output.ark.utt1'
utt2lang_file='data/data_7lang/eval_short/utt2lang1'
output_file='error_tmp.txt'
#utt2lang=os.listdir(utt2lang_file)
#files=os.listdir(wav_file)
langID = ('it', 'hi', 'jw', 'ko', 'pt', 'us', 'uk')
ID2ind = {'it':0, 'hi':1, 'jw':2, 'ko':3, 'pt':4, 'us':5, 'uk':6}
count=0
file1 = open(utt2lang_file, 'r')
utt2lang = file1.readlines()
trueth={}
for line in utt2lang:
    trueth[line.split()[0]]=(line.split()[1])
i=0
file2 = open(wav_file, 'r')
files = file2.readlines()
f_error = open(output_file, 'a')
for line in files:
    ID = line.split()[0]
    sn = line.split()[1:8]
    scores=[]
    for n in sn:
        scores.append(float(n))
    #score=scores[0]
    
    maxpos = scores.index(max(scores))
    if langID[maxpos] == trueth[ID]:
        count=count+1
    else:
        str1=" "
        outline= trueth[ID] + str(ID2ind[trueth[ID]]) + ' ' + ID + ' ' + str1.join(sn) + ' ' + langID[maxpos] + str(maxpos) + '\n'
        f_error.write(outline)
        

print('')    
     


