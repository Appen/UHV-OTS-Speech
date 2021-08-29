#!/bin/bash

cmd="run.pl"
. ./cmd.sh
. ./path.sh

stage=
. utils/parse_options.sh

dir=exp/xvectors_train_5000_33lang_cosine
#data=data/eval
dir_enrol=exp/xvectors_train_5000_33lang_cosine
data_enrol=data/train_5000_33lang
dir_test=exp/xvectors_dev_cosine
data_test=data/dev

trials=$data_test/trials_33

$train_cmd $dir/scoring.log \
    ivector-plda-scoring --normalize-length=true \
    --num-utts=ark:$dir_enrol/num_utts.ark \
    "ivector-copy-plda --smoothing=0.0 $dir/plda - |" \
    "ark:ivector-mean ark:$data_enrol/spk2utt scp:$dir_enrol/vector.scp ark:- | ivector-subtract-global-mean $dir/mean.vec ark:- ark:- | transform-vec $dir/transform.mat ark:- ark:- | ivector-normalize-length ark:- ark:- |" \
    "ark:ivector-subtract-global-mean $dir/mean.vec scp:$dir_test/vector.scp ark:- | transform-vec $dir/transform.mat ark:- ark:- | ivector-normalize-length ark:- ark:- |" \
    "cat $trials | cut -d\  --fields=1,2 |" exp/scores/plda_scores_33_new || exit 1;


compute-eer <(python3 local/prepare_for_eer.py $trials exp/scores/plda_scores_33_new) 
