#!/bin/bash

. ./path.sh || exit 1;
. ./cmd.sh || exit 1;

if [ $# -ne 6 ]; then
  echo $#
  echo "Wrong number of parameter"
  echo "Usage: ./run_lm_test_after_training_chain.sh train_dir lm_dir lm_data build_lang mk_graph "
  exit 1
fi

asr_traindir=$1
lang=${asr_traindir}/data/lang
lm_dir=$2
lm_date=lm_$3
testdir=./data/
#data/test_data/
testset=$4

nj=`nproc`

nnet3_affix=_cleaned
build_lang=$5
mk_graph=$6
#last_tri=$5


if [ $build_lang -eq 1 ]; then 
  
  tmpdir=data/local/lm_tmp.$$
  trap "rm -r $tmpdir" EXIT

  mkdir -p $tmpdir

  for lm_suffix in tgsmall; do
    # tglarge is prepared by a separate command, called from run.sh; we don't
    # want to compile G.fst for tglarge, as it takes a while.
    test=${lang}_test_${lm_suffix}_${lm_date}
    echo $test
    echo ${lang}
    mkdir -p $test
    cp -r ${lang}/* $test
    gunzip -c ${lm_dir}/lm_${lm_suffix}.arpa.gz | arpa2fst --disambig-symbol=#0 --read-symbol-table=$test/words.txt - $test/G.fst
    utils/validate_lang.pl --skip-determinization-check $test || exit 1;
  done

  utils/build_const_arpa_lm.sh ${lm_dir}/lm_tglarge.arpa.gz $lang ${lang}_test_tglarge_${lm_date}
  utils/build_const_arpa_lm.sh ${lm_dir}/lm_fglarge.arpa.gz $lang ${lang}_test_fglarge_${lm_date}
  utils/build_const_arpa_lm.sh ${lm_dir}/lm_vglarge.arpa.gz $lang ${lang}_test_vglarge_${lm_date}
fi


if [ $mk_graph -eq 1 ]; then
  echo "Start to make graph"
  utils/mkgraph.sh --self-loop-scale 1.0 --remove-oov ${lang}_test_tgsmall_${lm_date} ${asr_traindir}/exp/chain_cleaned/tdnn_cnn_1a_sp/ ${asr_traindir}/exp/chain_cleaned/tdnn_cnn_1a_sp/graph_tgsmall_${lm_date}
fi

spkr_num_in_test=`wc -l < ${testdir}/${testset}_hires/spk2utt`
echo "$spkr_num_in_test speakers in test set $testset"

if [ "$spkr_num_in_test" -lt $nj ]; then
  decode_nj=$spkr_num_in_test
else
  decode_nj=$nj
fi



steps/online/nnet2/extract_ivectors_online.sh --cmd "$train_cmd" --nj $decode_nj ${testdir}/${testset}_hires ${asr_traindir}/exp/nnet3${nnet3_affix}/extractor ${asr_traindir}/exp/nnet3${nnet3_affix}/ivectors_${testset}_hires || exit 1;


dir=${asr_traindir}/exp/chain_cleaned/tdnn_cnn_1a_sp


steps/nnet3/decode.sh --acwt 1.0 --post-decode-acwt 10.0 --nj $decode_nj --cmd "$decode_cmd"  --online-ivector-dir ${asr_traindir}/exp/nnet3${nnet3_affix}/ivectors_${testset}_hires ${asr_traindir}/exp/chain_cleaned/tdnn_cnn_1a_sp/graph_tgsmall_${lm_date} ${testdir}/${testset}_hires $dir/decode_${testset}_hires_tgsmall_${lm_date} || exit 1

  

steps/lmrescore_const_arpa.sh --cmd "$decode_cmd" ${lang}_test_{tgsmall,tglarge}_${lm_date} ${testdir}/${testset}_hires $dir/decode_${testset}_hires_{tgsmall,tglarge}_${lm_date} || exit 1
steps/lmrescore_const_arpa.sh --cmd "$decode_cmd" ${lang}_test_{tgsmall,fglarge}_${lm_date} ${testdir}/${testset}_hires $dir/decode_${testset}_hires_{tgsmall,fglarge}_${lm_date} || exit 1
steps/lmrescore_const_arpa.sh --cmd "$decode_cmd" ${lang}_test_{tgsmall,vglarge}_${lm_date} ${testdir}/${testset}_hires $dir/decode_${testset}_hires_{tgsmall,vglarge}_${lm_date} || exit 1

echo "Done Offline Test "
grep WER $dir/decode_${testset}_hires_*_${lm_date}/wer_* | utils/best_wer.sh

#steps/online/nnet3/prepare_online_decoding.sh --mfcc-config conf/mfcc_hires.conf ${lang}_test_tgsmall_${lm_date} ${asr_traindir}/exp/nnet3${nnet3_affix}/extractor $dir ${dir}_online
