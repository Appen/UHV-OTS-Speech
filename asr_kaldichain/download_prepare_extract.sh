#!/bin/bash
. ./path.sh
. ./cmd.sh

data_url=www.openslr.org/resources/12
data=/data/
mfccdir=mfcc
mkdir -p $data

for part in test-clean test-other; do
  local/download_and_untar.sh $data $data_url $part
done

for part in test-clean test-other; do
  # use underscore-separated names in data directories.
  local/data_prep.sh $data/LibriSpeech/$part data/$(echo $part | sed s/-/_/g)
done

for part in test_clean test_other; do
  steps/make_mfcc.sh --cmd "$train_cmd" --nj 40 data/$part exp/make_mfcc/$part $mfccdir || exit 1;
  steps/compute_cmvn_stats.sh data/$part exp/make_mfcc/$part $mfccdir || exit 1;
done


for datadir in test_clean test_other; do
  utils/copy_data_dir.sh data/$datadir data/${datadir}_hires
  steps/make_mfcc.sh --nj 70 --mfcc-config conf/mfcc_hires.conf \
      --cmd "$train_cmd" data/${datadir}_hires exp/make_hires/$datadir $mfccdir || exit 1;
  steps/compute_cmvn_stats.sh data/${datadir}_hires exp/make_hires/$datadir $mfccdir || exit 1;
done
