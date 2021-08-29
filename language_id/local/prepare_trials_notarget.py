#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2018  Tsinghua University (Author: Zhiyuan Tang)


import sys, collections

if len(sys.argv) != 3:
  print ('usage: prepare_trials.py <enroll-dir> <test-dir>')
  sys.exit()

enroll_dir = sys.argv[1]
test_dir = sys.argv[2]

# lang list in enroll dir
lang_list = []
with open(enroll_dir + '/utt2lang', 'r') as langs:
  for line in langs:
    lang_list.append(line.strip().split()[1])
lang_list = list(set(lang_list))
lang_list.sort()

# utt2lang dict in test dir
#lang_dict = collections.OrderedDict()
test_lst = []
with open(test_dir + '/wav.scp', 'r') as wav_ids:
  for wav_id in [line.strip().split() for line in wav_ids]:
     #lang_dict[lang_id[0]] = lang_id[1]
     test_lst.append(wav_id[0])

# generate trials
trial = open(test_dir + '/trials_notarget', 'w')

for i in test_lst:
  for j in lang_list:
    #if j == lang_dict[i]:
      trial.write(j + ' ' + i + '\n')
    #else:
    #  trial.write(j + ' ' + i + ' ' + 'nontarget' + '\n')

print('Finished preparing trials.')
