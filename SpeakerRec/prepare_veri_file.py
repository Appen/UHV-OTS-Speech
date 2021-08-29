#!/usr/bin/python3

input_file = 'veri_test.txt'
f = open(input_file, 'r')

output_file = 'results/voxceleb1_2/speaker_verification_ecapa_big/save/veri_test2_spk.txt'
fo = open(output_file, 'a')

for line in f.readlines():
    items = line.strip().split()
    real = items[0]
    spk_id = items[1].split('/')[0]
    utt = items[2]
    outline = real + ' ' + spk_id + ' ' + utt + '\n'
    fo.write(outline)


