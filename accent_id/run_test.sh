#!/bin/bash

cmd="run.pl"
. ./cmd.sh
. ./path.sh

stage=
. utils/parse_options.sh

dir=exp/xvectors_train_20000
dir_enrol=exp/xvectors_train_20000
data_enrol=data/train_20000
dir_test=exp/xvectors_test_20000
data_test=data/test_20000
trials=$data_test/trials

$train_cmd $dir/scoring.log \
    ivector-plda-scoring --normalize-length=true \
     --num-utts=ark:$dir_enrol/num_utts.ark \
      "ivector-copy-plda --smoothing=0.0 $dir/plda - |" \
      "ark:ivector-mean ark:$data_enrol/spk2utt scp:$dir_enrol/vector.scp ark:- | ivector-subtract-global-mean $dir/mean.vec ark:- ark:- | transform-vec $dir/transform.mat ark:- ark:- | ivector-normalize-length ark:- ark:- |" \
       "ark:ivector-subtract-global-mean $dir/mean.vec scp:$dir_test/vector.scp ark:- | transform-vec $dir/transform.mat ark:- ark:- | ivector-normalize-length ark:- ark:- |" \
       "cat $trials | cut -d\  --fields=1,2 |" exp/scores/plda_scores || exit 1;
echo "Done calculation"
compute-eer <(python3 local/prepare_for_eer.py $trials exp/scores/plda_scores)
