#!/usr/bin/python3

import os,sys
import glob
import wave
import wave
import contextlib
import subprocess

if len(sys.argv)!= 3:
    print("Usage: python3 run_spleeter.py [audio_dir] [output_dir]")
    exit()

audio_dir= sys.argv[1]
out_dir = sys.argv[2]

all_wav = glob.glob(audio_dir+'/*.wav')
for fname in all_wav:
    dur = 0
    with contextlib.closing(wave.open(fname,'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = (frames / float(rate))
        #print(duration)
        #print(round(duration))
    
        if round(duration) < duration:
            dur  = round(duration)+1
        else:
            dur = round(duration)

        #print(dur)
    print("Separating for file: " + fname)
    cmd_ln = 'spleeter separate -B librosa -p spleeter:2stems '+' -d '+str(duration)+ ' -o '+out_dir + ' ' +fname
    p = subprocess.Popen(cmd_ln,shell=True, stdout=subprocess.PIPE)
    p.wait()
    print(p.returncode)

    #sox accompaniment.wav -c 1 -r 16000 -b 16 n_49QZZK-WU_bgm.wav 
    file_id=  fname.split('/')[-1].split('.wav')[0]
    bgm_441= out_dir+'/'+file_id+'/accompaniment.wav'
    bgm_f =  out_dir+'/'+file_id+'/'+file_id+'_bgm.wav'
    print("Converting accompaniment to 16000Hz 16bit wav file in to "+ bgm_f)
    cmd_ln = 'sox '+bgm_441+' -c 1 -r 16000 -b 16 '+bgm_f
    p = subprocess.Popen(cmd_ln,shell=True, stdout=subprocess.PIPE)
    p.wait()
    print(p.returncode)
    
    speech_441 = out_dir+'/'+file_id+'/vocals.wav'
    speech_f = out_dir+'/'+file_id+'/'+file_id+'_speech.wav'
    print("Converting vocals to 16000Hz 16bit wav file in to "+ speech_f)
    cmd_ln = 'sox '+speech_441+' -c 1 -r 16000 -b 16 '+speech_f
    p = subprocess.Popen(cmd_ln,shell=True, stdout=subprocess.PIPE)
    p.wait()
    print(p.returncode)

    os.remove(bgm_441)
    os.remove(speech_441)



    
    
