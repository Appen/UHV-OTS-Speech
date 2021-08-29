#!/usr/bin/env python3
import os

input_file='exp/scores/plda_scores_5s_33'
output_file='exp/scores/output.ark.utt'
ID_file='data/dev/ID'

#langID = ('ba', 'bs', 'es', 'as', 'jw', 'tk', 'sq', 'tt', 'sr', 'tg', 'zh', 'mr', 'nl', 'ko', 'az', 'gu', 'kn', 'cy', 'lv', 'pl', 'hy', 'hi', 'su', 'gl', 'sv', 'ht', 'be', 'ja', 'mt', 'is', 'ms', 'km', 'af', 'sd', 'hr', 'mg', 'kk', 'hu', 'lo', 'cs', 'ps', 'my', 'tr', 'bg', 'bo', 'mn', 'pa', 'tl', 'ca', 'iw', 'fi', 'yi', 'sk', 'no', 'eu', 'yo', 'sw', 'ha', 'ml', 'en', 'et', 'ta', 'ro', 'th', 'mi', 'vi', 'fa', 'ka', 'fo', 'de', 'so', 'am', 'lt', 'id', 'sl', 'el', 'sn', 'br', 'lb', 'mk', 'it', 'te', 'ne', 'ru', 'uz', 'fr', 'bn', 'ur', 'nn', 'da', 'ln', 'si', 'la', 'ar', 'uk', 'pt')

langID = ('ar', 'az', 'da', 'de', 'el', 'en', 'es', 'et', 'fa', 'fi', 'fr', 'hr', 'hu', 'hy', 'is', 'it', 'ja', 'lt', 'lv', 'mk', 'nl', 'nn', 'no', 'pl', 'pt', 'ru', 'sl', 'sr', 'sv', 'tr', 'uk', 'ur', 'zh')
file1 = open(ID_file, 'r')
IDs=file1.readlines()

Dict = {}
for ID in IDs:
    Dict[ID.rstrip()]={}

f_out = open(output_file, 'a')

file2 = open(input_file, 'r')
files = file2.readlines()
for line in files:
    uttID=line.split()[1]
    lID=line.split()[0]
    Dict[uttID][lID]=line.split()[2]

for utt in IDs:
    utt=utt.rstrip()
    outline=utt
    for lang in langID:
        outline = outline + ' ' + str(Dict[utt][lang])

    outline = outline + '\n'
    f_out.write(outline)
         
f_out.close()
    



