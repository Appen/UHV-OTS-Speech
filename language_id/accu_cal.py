#!/usr/bin/env python3
import os

wav_file='exp/scores/output.ark.utt'
utt2lang_file='data/dev/utt2lang'
output_file='error_tmp.txt'
output_file2='correct_temp.txt'
#utt2lang=os.listdir(utt2lang_file)
#files=os.listdir(wav_file)
#langID = ('it', 'hi', 'jw', 'ko', 'pt', 'us', 'uk')
#langID = ('ba', 'bs', 'es', 'as', 'jw', 'tk', 'sq', 'tt', 'sr', 'tg', 'zh', 'mr', 'nl', 'ko', 'az', 'gu', 'kn', 'cy', 'lv', 'pl', 'hy', 'hi', 'su', 'gl', 'sv', 'ht', 'be', 'ja', 'mt', 'is', 'ms', 'km', 'af', 'sd', 'hr', 'mg', 'kk', 'hu', 'lo', 'cs', 'ps', 'my', 'tr', 'bg', 'bo', 'mn', 'pa', 'tl', 'ca', 'iw', 'fi', 'yi', 'sk', 'no', 'eu', 'yo', 'sw', 'ha', 'ml', 'en', 'et', 'ta', 'ro', 'th', 'mi', 'vi', 'fa', 'ka', 'fo', 'de', 'so', 'am', 'lt', 'id', 'sl', 'el', 'sn', 'br', 'lb', 'mk', 'it', 'te', 'ne', 'ru', 'uz', 'fr', 'bn', 'ur', 'nn', 'da', 'ln', 'si', 'la', 'ar', 'uk', 'pt')

langID = ('ar', 'az', 'da', 'de', 'el', 'en', 'es', 'et', 'fa', 'fi', 'fr', 'hr', 'hu', 'hy', 'is', 'it', 'ja', 'lt', 'lv', 'mk', 'nl', 'nn', 'no', 'pl', 'pt', 'ru', 'sl', 'sr', 'sv', 'tr', 'uk', 'ur', 'zh')
#ID2ind = {'it':0, 'hi':1, 'jw':2, 'ko':3, 'pt':4, 'us':5, 'uk':6}
#ID2ind = {'ba':0, 'bs':1, 'es':2, 'as':3, 'jw':4, 'tk':5, 'sq':6, 'tt':7, 'sr':8, 'tg':9, 'zh':10, 'mr':11, 'nl':12, 'ko':13, 'az':14, 'gu':15, 'kn':16, 'cy':17, 'lv':18, 'pl':19, 'hy':20, 'hi':21, 'su':22, 'gl':23, 'sv':24, 'ht':25, 'be':26, 'ja':27, 'mt':28, 'is':29, 'ms':30, 'km':31, 'af':32, 'sd':33, 'hr':34, 'mg':35, 'kk':36, 'hu':37, 'lo':38, 'cs':39, 'ps':40, 'my':41, 'tr':42, 'bg':43, 'bo':44, 'mn':45, 'pa':46, 'tl':47, 'ca':48, 'iw':49, 'fi':50, 'yi':51, 'sk':52, 'no':53, 'eu':54, 'yo':55, 'sw':56, 'ha':57, 'ml':58, 'en':59, 'et':60, 'ta':61, 'ro':62, 'th':63, 'mi':64, 'vi':65, 'fa':66, 'ka':67, 'fo':68, 'de':69, 'so':70, 'am':71, 'lt':72, 'id':73, 'sl':74, 'el':75, 'sn':76, 'br':77, 'lb':78, 'mk':79, 'it':80, 'te':81, 'ne':82, 'ru':83, 'uz':84, 'fr':85, 'bn':86, 'ur':87, 'nn':88, 'da':89, 'ln':90, 'si':91, 'la':92, 'ar':93, 'uk':94, 'pt':95}

ID2ind = {'ar':0, 'az':1, 'da':2, 'de':3, 'el':4, 'en':5, 'es':6, 'et':7, 'fa':8, 'fi':9, 'fr':10, 'hr':11, 'hu':12, 'hy':13, 'is':14, 'it':15, 'ja':16, 'lt':17, 'lv':18, 'mk':19, 'nl':20, 'nn':21, 'no':22, 'pl':23, 'pt':24, 'ru':25, 'sl':26, 'sr':27, 'sv':28, 'tr':29, 'uk':30, 'ur':31, 'zh':32}

#ind2ID = {0:'ba', 1:'bs', 2:'es', 3:'as', 4:'jw', 5:'tk', 6:'sq', 7:'tt', 8:'sr', 9:'tg', 10:'zh', 11:'mr', 12:'nl', 13:'ko', 14:'az', 15:'gu', 16:'kn', 17:'cy', 18:'lv', 19:'pl', 20:'hy', 21:'hi', 22:'su', 23:'gl', 24:'sv', 25:'ht', 26:'be', 27:'ja', 28:'mt', 29:'is', 30:'ms', 31:'km', 32:'af', 33:'sd', 34:'hr', 35:'mg', 36:'kk', 37:'hu', 38:'lo', 39:'cs', 40:'ps', 41:'my', 42:'tr', 43:'bg', 44:'bo', 45:'mn', 46:'pa', 47:'tl', 48:'ca', 49:'iw', 50:'fi', 51:'yi', 52:'sk', 53:'no', 54:'eu', 55:'yo', 56:'sw', 57:'ha', 58:'ml', 59:'en', 60:'et', 61:'ta', 62:'ro', 63:'th', 64:'mi', 65:'vi', 66:'fa', 67:'ka', 68:'fo', 69:'de', 70:'so', 71:'am', 72:'lt', 73:'id', 74:'sl', 75:'el', 76:'sn', 77:'br', 78:'lb', 79:'mk', 80:'it', 81:'te', 82:'ne', 83:'ru', 84:'uz', 85:'fr', 86:'bn', 87:'ur', 88:'nn', 89:'da', 90:'ln', 91:'si', 92:'la', 93:'ar', 94:'uk', 95:'pt'}

ind2ID = {0:'ar', 1:'az', 2:'da', 3:'de', 4:'el', 5:'en', 6:'es', 7:'et', 8:'fa', 9:'fi', 10:'fr', 11:'hr', 12:'hu', 13:'hy', 14:'is', 15:'it', 16:'ja', 17:'lt', 18:'lv', 19:'mk', 20:'nl', 21:'nn', 22:'no', 23:'pl', 24:'pt', 25:'ru', 26:'sl', 27:'sr', 28:'sv', 29:'tr', 30:'uk', 31:'ur', 32:'zh'}
count=0
file1 = open(utt2lang_file, 'r')
utt2lang = file1.readlines()
trueth={}
for line in utt2lang:
    trueth[line.split()[0]]=(line.split()[1])
i=0
file2 = open(wav_file, 'r')
files = file2.readlines()
f_error = open(output_file, 'w')
f_correct = open(output_file2, 'w')
for line in files[1:]:
    ID = line.split()[0]
    sn = line.split()[1:97]
    scores=[]
    for n in sn:
        scores.append(float(n))
    #score=scores[0]
    
    maxpos = scores.index(max(scores))
    if langID[maxpos] == trueth[ID]:
        count=count+1
        outline=trueth[ID] + ' '+ str(ID2ind[trueth[ID]]) + ' ' + ID + ' '+ str(max(scores)) + ' '+ ind2ID[maxpos] + ' '+ str(maxpos) + '\n'
        f_correct.write(outline)
    else:
        str1=" "
        #outline= trueth[ID] + ' '+ str(ID2ind[trueth[ID]]) + ' ' + ID + ' ' +  str1.join(sn) + ' ' + ind2ID[maxpos] + ' '+ str(maxpos) + '\n'
        #f_error.write(outline)
        outline = trueth[ID] + ' ' + str(ID2ind[trueth[ID]]) + ' '+ str(scores[ID2ind[trueth[ID]]]) + ' ' + str(maxpos) + ' '+ ind2ID[maxpos] + ' '+str(scores[maxpos]) + '\n'
        f_error.write(outline)
        

print('')    
     


