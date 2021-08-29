#!/usr/bin/env python3
import numpy as np
import os
import sys

feat5s_file='tmp_long.lst'
outfile = 'feat_papralle.lst'
utt2lang_file = 'utt2lang'

fs=open(feat5s_file, 'r')
#feat_short=fs.read_lines()

fo=open(outfile, 'a')
fl=open(utt2lang_file, 'a')

for line in fs:
    idx = line.strip().split()[0]
    ID = line.strip().split()[1]
    feat = line.strip().split()[2]
    lang = line.strip().split()[4]

    if int(idx)%2 == 1:
        outline = ""
        outline = idx + ' '+ ID + ' ' + feat
        line_lang = ID + ' ' + lang + '\n'
        fl.write(line_lang)
        

    else:
        outline =outline + ' ' + feat + '\n'
        fo.write(outline)

