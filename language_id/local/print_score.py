#!/usr/bin/env python3

score_file='exp/xvector_eval/output.ark.utt1'
output_file='outset.txt'
file1 = open(score_file, 'r')
for line in file1:
    scores = line.split()[1:8]
    ss=[]
    for i in scores:
        ss.append(float(i))
    maxscore = max(ss)
    print(maxscore)

