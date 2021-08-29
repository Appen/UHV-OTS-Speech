This is the demo scripts for running the benchmarking test or run with real project data.

This module is to detect the synthetic speech or, so called spoofed speedh. 
The algorithm used in this module was proposed in [Towards end-to-end synthetic speech detection] (https://arxiv.org/abs/2106.06341). The original repo is hosted in [github repo](https://github.com/ghuawhu/end-to-end-synthetic-speech-detection.git). 

To replicate the orginal experimental results, please follow the originla repo's scripts. To download the ASVspoof2015 and ASVspoof2019 datasets, please run the ./download.sh script.

In this module, we utlize the the pretrained res-TSSD net from original repo. The model file is: Res_TSSDNet_time_frame_61_ASVspoof2019_LA_Loss_0.0017_dEER_0.74%_eEER_1.64%.pth. 

./run_demo.py is the script to run the module on given input audio folder and output the corresponding results. 

./syn_speech_e2e_s3_test.py is the script called by ./run_demo.py to conduct the demo. It was heritaged from test.py in original repo.

./data folder contains the sample audio files and needed list files to run the demo. 

After the demo running, there will be an output file ./systhetic_speech_test_result.csv, it looks like:
'''
audio_file_name,class_label,probability
LA_D_1047731.flac,bonafide,0.9999999
LA_D_1105538.flac,bonafide,1.0
LA_D_1125976.flac,bonafide,1.0
''' 
