This is the speaker diarization system developed based on BUT's diarization system introduced in [Analysis of the BUT Diarization System for VoxConverse Challenge](https://arxiv.org/abs/2010.11718).

The speaker diarization framework generally involves an embedding stage followed by a clustering stage.

We tested the pipeline with [VoxConverse corpus](http://www.robots.ox.ac.uk/~vgg/data/voxconverse), which is an audio-visual diarization dataset consisting of over 50 hours of multi-speaker clips of human speech, extracted from videos collected on the internet.  The DER achieved on VoxConverse using the BUT system is 4.41%, which is consistent with the result in BUT's report.

To download the dataset, please run the command as in following:
```bash
cd speaker_diarization
./download.sh
```
After the data downloading, please run the test on VoxConverse data by running the commands in below:
```bash
./run_test.sh
```

