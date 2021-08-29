#!/bin/bash

cmd="run.pl"
. ./cmd.sh
. ./path.sh

stage=
. utils/parse_options.sh

if [ $stage -le 0 ]; then
  train_dir=data/train_20000
  mv $train_dir/utt2spk $train_dir/utt2spk.bak  
  mv $train_dir/spk2utt $train_dir/spk2utt.bak 
  cp $train_dir/utt2lang $train_dir/utt2spk
  utils/utt2spk_to_spk2utt.pl $train_dir/utt2spk > $train_dir/spk2utt
  utils/fix_data_dir.sh $train_dir
fi

if [ $stage -le 1 ]; then
   train_dir=data/train_20000
   train_nosil_dir=data/train_20000_no_sil
   exp_dir=exp/train_20000_no_sil
   local/nnet3/xvector/prepare_feats_for_egs.sh --nj 30 --cmd "$train_cmd" \
       $train_dir $train_nosil_dir $exp_dir
   utils/fix_data_dir.sh $train_nosil_dir 

fi

if [ $stage -le 2 ]; then
  sudo nvidia-smi -c 3
  nnet_dir=exp/xvect_20000
  local/nnet3/xvector/run_xvector.sh --stage 6 --train-stage -1 \
      --data data/train_20000_no_sil --nnet-dir $nnet_dir \
      --egs-dir $nnet_dir/egs

fi

#exit 0

if [ $stage -le 9 ]; then
nnet_dir=exp/xvect_20000
dir_enrol=exp/xvectors_train_20000
data_enrol=data/train_20000
dir_test=exp/xvectors_test_20000_10s
data_test=data/test_20000_10s
#local/nnet3/xvector/extract_xvectors.sh --cmd "$train_cmd --mem 6G" --nj 10 \
    $nnet_dir $data_enrol $dir_enrol
local/nnet3/xvector/extract_xvectors.sh --cmd "$train_cmd --mem 6G" --nj 10 \
        $nnet_dir $data_test $dir_test
fi




#PLDA
if [ $stage -le 10 ]; then
    dir=exp/xvectors_train_20000
    data=data/train_20000
    $cmd $dir/log/vector.log \
          ivector-mean  scp:$dir/vector.scp  $dir/mean.vec
     echo "average done"  
fi

if [ $stage -le 11 ]; then
    dir=exp/xvectors_train_20000
    data=data/train_20000
    lda_dim=20
    $train_cmd exp/xvectors_train_20000/log/lda.log \
        ivector-compute-lda --total-covariance-factor=0.0 --dim=$lda_dim \
        "ark:ivector-subtract-global-mean scp:$dir/vector.scp ark:- |" \
        ark:$data/utt2spk $dir/transform.mat
    $train_cmd $dir/log/plda.log \
        ivector-compute-plda ark:$data/spk2utt \
        "ark:ivector-subtract-global-mean scp:$dir/vector.scp ark:- | transform-vec $dir/transform.mat ark:- ark:- | ivector-normalize-length ark:-  ark:- |" \
         $dir/plda || exit 1;
    echo "plda train done"
fi

if [ $stage -le 12 ]; then
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


fi

exit 0

if [ $stage -le 13 ]; then
    train_dir=exp/xvectors_train_20000
    train_data_dir=data/train_20000
    test_dir=exp/xvectors_test_20000
    test_data_dir=data/test_20000
    train_ivectors="ark:ivector-subtract-global-mean scp:$train_dir/vector.scp ark:- | ivector-normalize-length ark:-  ark:- |"
    test_ivectors="ark:ivector-subtract-global-mean scp:$test_dir/vector.scp ark:- | ivector-normalize-length ark:-  ark:- |"
    classes="ark:utils/sym2int.pl -f 2 exp/xvect/lang2lang_id $train_data_dir/utt2spk |"
    model_dir=exp/model_regression
    model="$model_dir/regression"
    apply_log=true
    trials=$test_data_dir/trials
    languages=exp/xvect/lang2lang_id
    logistic-regression-train --config=$conf "$train_ivectors" \
        "$classes" $model \
        2>$model_dir/log/logistic_regression.log
    logistic-regression-eval --apply-log=$apply_log $model   "$test_ivectors" ark,t:$test_dir/posteriors
    x=`head -1 $test_dir/output.ark.utt`
    sed -i "1s/^/$x\n /"  $test_dir/posteriors
    sed -i -e 's|\[||; s|\]||' $test_dir/posteriors
    eer=`compute-eer <(python local/nnet3/prepare_for_eer.py $trials $test_dir/posteriors) 2> /dev/null`
    echo $eer
fi




