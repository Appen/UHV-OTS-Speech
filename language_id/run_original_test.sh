#!/bin/bash

. ./cmd.sh
. ./path.sh

audio_list=
window=
. utils/parse_options.sh

rm -r data_test
mkdir -p data_test
rm -r mfcc_test
mkdir -p mfcc_test
fileNo=`wc -l $audio_list`
nnet_dir=exp/xvect
dir=model

if[$window == false];then
    nl $audio_list | perl -lane 'print "S@F"'> data_test/wav.scp
    cat data_test/wav.scp | awk '{print $1 "\t" $1}' > data_test/utt2spk
    utils/utt2spk_to_spk2utt.pl data_test/utt2spk > data_test/spk2utt

    steps/make_mfcc.sh --write-utt2num-frames true --mfcc-condif conf/mfcc_hires_16k.conf --nj 1 --cmd "$train_cmd" data_test exp/make_mfcc mfcc_test
    sid/compute_vad_decision.sh --cmd "$train_cmd" --nj 1 data_test exp/make_vad vad_test
    #local/run_xvect_score.sh --cmd "$train_cmd" --nj 1 $nnet_dir data_test exp/xvectors_test
    local/nnet3/xvector/extract_xvectors.sh --cmd "$train_cmd --mem 6G" --nj 1 \
        $nnet_dir data_test  exp/xvectors_test
    $train_cmd $dir/scoring.log \
         ivector-plda-scoring --normalize-length=true \
         --num-utts=ark:$dir/num_utts.ark \
         "ivector-copy-plda --smoothing=0.0 $dir/plda - |" \
         $dir/ivector_mean.ark \
         "ark:ivector-subtract-global-mean $dir/mean.vec scp:exp/xvectors_test/vector.scp ark:- | transform-vec $dir/transform.mat ark:- ark:- | ivector-normalize-length ark:- ark:- |" \
         "cat $trials | cut -d\  --fields=1,2 |" results/plda_scores || exit 1;
    python score2output.py 

#    sudo sed -i '1d' exp/xvectors_test/output.ark.utt

    sudo python3 print_results.py
else
    nl $audio_list | perl -lane 'print "S@F"'> data_test/wav.scp
    soxi -D `awk '{print $2}'` | paste data_test/wav.scp - | awk '{print $1 " " $2}' > data_test/utt2dur
    python  segment_create.py  
    
    steps/make_mfcc.sh --write-utt2num-frames true --mfcc-config conf/mfcc_hires_16k.conf --nj 1 --cmd "$train_cmd" data_test exp/make_mfcc mfcc_test
    sid/compute_vad_decision.sh --cmd "$train_cmd" --nj 1 data_test exp/make_vad vad_test
    local/nnet3/xvector/extract_xvectors.sh --cmd "$train_cmd --mem 6G" --nj 1 \
                $nnet_dir data_test  exp/xvectors_test

    $train_cmd $dir/scoring.log \
         ivector-plda-scoring --normalize-length=true \
         --num-utts=ark:$dir/num_utts.ark \
         "ivector-copy-plda --smoothing=0.0 $dir/plda - |" \
         $dir/ivector_mean.ark \
         "ark:ivector-subtract-global-mean $dir/mean.vec scp:exp/xvectors_test/vector.scp ark:- | transform-vec $dir/transform.mat ark:- ark:- | ivector-normalize-length ark:- ark:- |" \
         "cat $trials | cut -d\  --fields=1,2 |" results/plda_scores || exit 1; 
    python score2output.py
    python print_results_wiindow.py





