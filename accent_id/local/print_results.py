#!/usr/bin/env python3
import os


score_file='exp/xvectors_test/output.ark.utt'
wav_file='data_test/wav.scp'
result_file='exp/xvectors_test/result'
if os.path.exists(result_file):
    os.remove(result_file)
fileRe = open(result_file, 'a')

langID = ('Italian', 'Hindi', 'Japaness', 'Korean', 'Portuguese', 'Enlighs_US', 'English_UK')

file1 = open(wav_file, 'r')
wavfiles = file1.readlines()
ID2utt={}
for line in wavfiles:
    ID2utt[line.split()[0]]=line.split()[1:-1]
file2 = open(score_file, 'r')
files = file2.readlines()
for line in files:
    ID = line.split()[0]
    sn = line.split()[1:8]
    scores=[]
    for n in sn:
        scores.append(float(n))
    maxpos = scores.index(max(scores))
    uttID = ' '.join([str(elem) for elem in ID2utt[ID]])
    outline = uttID + ': ' + langID[maxpos] + '\n'
    fileRe.write(outline)


