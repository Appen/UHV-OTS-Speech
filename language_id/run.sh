#!/bin/bash

cmd="run.pl"
. ./cmd.sh
. ./path.sh

stage=
. utils/parse_options.sh

# prepare data

if [ $stage -le 0 ]; then
    voxdata_dir='/data8/voxlingua107/data/16k'
    langID=`ls $voxdata_dir | grep -v 'ab\|ceb\|eo\|gn\|gv\|haw\|ia\|oc\|sa\|sco\|war'`
    line_lang=''
    for i in $langID; do
        cp ${voxdata_dir}/$i/feats_mfcc.scp ${voxdata_dir}/$i/feats.scp
        line_lang="$line_lang ${voxdata_dir}/$i"
    done
    utils/combine_data.sh data/train $line_lang
    utils/fix_data_dir.sh data/train
    utils/validate_data_dir.sh --no-text data/train
fi

#exit 0

# add some UK-English and US-English data
#not finsihed, not used
if [ $stage -le 1 ]; then  
    datadir='/home/ubuntu/src/kaldi/egs/lid/v1/data'
    mfccdir='/home/ubuntu/src/kaldi/egs/lid/v1/mfcc'
    vaddir='/home/ubuntu/src/kaldi/egs/lid/v1/mfcc'
    #datadir_us='/home/ubuntu/src/kaldi/egs/lid/v1/data/us_voxforge/train' 
    for lang in 'uk' 'us_voxforge'; do
        steps/make_mfcc.sh --write-utt2num-frames true --cmd "$train_cmd" --nj 40 $datadir/$lang/train exp/make_mfcc/$lang $mfccdir/$lang
        sid/compute_vad_decision.sh --nj 40 --cmd "$train_cmd" $datadir/$lang/train exp/make_vad/$lang $vaddir/$lang
        utils/fix_data_dir.sh $datadir/$lang/train
        utils/validate_data_dir.sh --no-text $datadir/$lang/train
    done
    cp -r $datadir/$lang/train data/train_$lang
    cp -r data/train data/train_voxlingua
    utils/combine_data.sh data/train data/train_voxlingua $datadir/uk/train $datadir/us_voxforge/train
 
fi

if [ $stage -le 2 ]; then
    mv data/train/utt2spk data/train/utt2spk.bak
    mv data/train/spk2utt data/train/spk2utt.bak
    cp data/train/utt2lang data/train/utt2spk
    utils/utt2spk_to_spk2utt.pl data/train/utt2spk > data/train/spk2utt
    utils/fix_data_dir.sh data/train

fi

if [ $stage -le 3 ]; then 
    local/nnet3/xvector/prepare_feats_for_egs.sh --nj 40 --cmd "$train_cmd"  data/train_small data/train_small_no_sil exp/train_samll_no_sil
    utils/fix_data_dir.sh data//train_small_no_sil    
fi


#remove features that are too short after removing silenceframes.
if [ $stage -le 4 ]; then
    min_len=50
    mv data/train_small_no_sil/utt2num_frames data/train_small_no_sil/utt2num_frames.bak
    awk -v min_len=${min_len} '$2 > min_len {print $1, $2}' data/train_small_no_sil/utt2num_frames.bak > data/train_small_no_sil/utt2num_frames
    utils/filter_scp.pl data/train_small_no_sil/utt2num_frames data/train_small_no_sil/utt2spk > data/train_small_no_sil/utt2spk.new
    mv data/train_small_no_sil/utt2spk.new data/train_small_no_sil/utt2spk
    utils/fix_data_dir.sh data/train_small_no_sil
    
fi



if [ $stage -le 5 ]; then
    sudo nvidia-smi -c 3
    nnet_dir=exp/xvect
    local/nnet3/xvector/run_xvector.sh --stage 4 --train-stage -1 \
        --data data/train_rest_no_sil --nnet-dir $nnet_dir \
        --egs-dir $nnet_dir/egs

fi

#exit 0

if [ $stage -le 6 ]; then
    for lang in ar  az  da  de  el  en  es  et  fa  fr  hr  hu  hy  is  it  ja  lt  lv  mk  nl  nn  no  pl  pt  ru  sl  sr  sv  tr  uk  ur  zh; do
        ls $PWD/data/dev/wavfile/$lang/* | perl -lane 'm|wavfile/.*/(.*).wav|; print "$1"' > ID_tmp
        ls $PWD/data/dev/wavfile/$lang/* | paste ID_tmp - >> data/dev/wav.scp
        paste ID_tmp ID_tmp >> data/dev/utt2spk
        cat ID_tmp | env lan=$lang perl -lane 'print "$F[0] $ENV{lan}"' >> data/dev/utt2lang
        soxi -D $(ls $PWD/data/dev/wavfile/$lang/*) | paste ID_tmp - >> data/dev/utt2dur

    done

fi

if [ $stage -le 7 ]; then 
    mfcc_config=conf/mfcc_hires_16k.conf
    steps/make_mfcc.sh --write-utt2num-frames true --cmd "$train_cmd" --nj 10 --mfcc-config $mfcc_config data/dev exp/make_mfcc/dev mfcc/dev
    sid/compute_vad_decision.sh --nj 10 --cmd "$train_cmd" data/dev exp/make_vad/dev mfcc/dev
    utils/fix_data_dir.sh data/dev
    utils/validate_data_dir.sh --no-text data/dev

fi


#local/run_xvect_score.sh --cmd "$train_cmd --mem 6G" --nj 10 \
#          $nnet_dir data_test_final/fbank/$x \
#                exp/xvectors_$x

if [ $stage -le 17 ]; then
        data=data/
            dir=exp/xvectors_eval
                trials=$data/eval/trials
                    #local/prepare_trials.py  $data/dev $data/eval_outset
                        local/cosine_scoring.sh $data/dev $data/eval exp/xvectors_dev/ exp/xvectors_eval $trials exp/xvectors_eval/scores

                    fi

#PLDA 19-21                    
if [ $stage -le 19 ]; then
    dir=exp/xvectors_eval_cosine
    data=data/eval
    $cmd $dir/log/vector.log \
        ivector-mean  scp:$dir/vector.scp \
        $dir/mean.vec
fi



if [ $stage -le 20 ]; then
    dir=exp/xvectors_eval_cosine
    dir_plda=exp/xvectors_train_5000_33lang
    data=data/eval
    data_plda=data/train_5000_33lang
    lda_dim=90
    $train_cmd exp/xvectors_eval_cosine/log/lda.log \
        ivector-compute-lda --total-covariance-factor=0.0 --dim=$lda_dim \
         "ark:ivector-subtract-global-mean scp:$dir/vector.scp ark:- |" \
         ark:$data/utt2spk $dir/transform.mat || exit 1;

    $train_cmd $dir/log/plda.log \
        ivector-compute-plda ark:$data_plda/spk2utt \
         "ark:ivector-subtract-global-mean scp:$dir_plda/vector.scp ark:- | transform-vec $dir/transform.mat ark:- ark:- | ivector-normalize-length ark:-  ark:- |" \
         $dir_plda/plda || exit 1;
fi

if [ $stage -le 21 ]; then
    #dir=exp/xvectors_eval_cosine
    dir=exp/xvectors_train_5000_33lang_cosine
    data=data/eval
    dir_enrol=exp/xvectors_train_5000_33lang_cosine
    data_enrol=data/train_5000_33lang
    dir_test=exp/xvectors_dev_cosine
    data_test=data/dev
    #dir_test=$dir_enrol
    #data_enrol=$data_enrol
    trials=$data_test/trials_33

    $train_cmd $dir/scoring.log \
        ivector-plda-scoring --normalize-length=true \
        --num-utts=ark:$dir_enrol/num_utts.ark \
        "ivector-copy-plda --smoothing=0.0 $dir/plda - |" \
        "ark:ivector-mean ark:$data_enrol/spk2utt scp:$dir_enrol/vector.scp ark:- | ivector-subtract-global-mean $dir/mean.vec ark:- ark:- | transform-vec $dir/transform.mat ark:- ark:- | ivector-normalize-length ark:- ark:- |" \
        "ark:ivector-subtract-global-mean $dir/mean.vec scp:$dir_test/vector.scp ark:- | transform-vec $dir/transform.mat ark:- ark:- | ivector-normalize-length ark:- ark:- |" \
         "cat $trials | cut -d\  --fields=1,2 |" exp/scores/plda_scores_33_new || exit 1;
    
fi
exit 0
#logistic regression backend 22

if [ $stage -le 22 ]; then
    train_dir=exp/xvectors_train_small
    train_data_dir=data/train_small
    test_dir=exp/xvectors_dev_cosine
    test_data_dir=data/dev
    train_ivectors="ark:ivector-subtract-global-mean scp:$train_dir/vector.scp ark:- | ivector-normalize-length ark:-  ark:- |"
    test_ivectors="ark:ivector-subtract-global-mean scp:$test_dir/vector.scp ark:- | ivector-normalize-length ark:-  ark:- |"
    classes="ark:utils/sym2int.pl -f 2 exp/xvect/lang2lang_id $train_data_dir/utt2spk |" 
    model_dir=exp/model_regression
    model="$model_dir/regression"
    apply_log=true
    #train_dir=$dir
    trials=$test_data_dir/trials
    languages=exp/xvect/lang2lang_id
    
    logistic-regression-train --config=$conf "$train_ivectors" \
                                  "$classes" $model \
                                     2>$model_dir/log/logistic_regression.log
    logistic-regression-eval --apply-log=$apply_log $model   "$test_ivectors" ark,t:$test_dir/posteriors
    #cat $test_dir/posteriors | awk '{max=$3; argmax=3; for(f=3;f<NF;f++) { if ($f>max) { max=$f; argmax=f; }} print $1, (argmax - 3); }' |  utils/int2sym.pl -f 2 $languages > $test_dir/output
    x=`head -1 exp/xvectors_eval/output.ark.utt`
    sed -i "1s/^/$x\n /"  $test_dir/posteriors
    sed -i -e 's|\[||; s|\]||' $test_dir/posteriors
    eer=`compute-eer <(python local/nnet3/prepare_for_eer.py $trials $test_dir/posteriors) 2> /dev/null`
    echo $eer

fi


