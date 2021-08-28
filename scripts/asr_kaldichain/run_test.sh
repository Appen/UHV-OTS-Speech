#!/bin/bash

if [ ! -f "/data/test-clean.tar.gz" ] 
then
  ./download_prepare_extract.sh
fi

train_dir=./
lm_dir=./data/local/lm/
lm_id=demo
test_set=test_other # test_other
build_lang=1
mk_graph=1
echo "./run_lm_test_after_training_chain.sh $train_dir $lm_dir $lm_data $test_set $build_lang $mk_graph"
./run_lm_test_after_training_chain.sh $train_dir $lm_dir $lm_id $test_set $build_lang $mk_graph 

test_set=test_clean
build_lang=0
mk_graph=0
./run_lm_test_after_training_chain.sh $train_dir $lm_dir $lm_id $test_set $build_lang $mk_graph
