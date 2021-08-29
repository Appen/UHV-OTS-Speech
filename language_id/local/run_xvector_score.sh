#!/bin/bash
#copyright     2017  David Snyder
#       2017  Johns Hopkins University (Author: Daniel Povey)
#       2017  Johns Hopkins University (Author: Daniel Garcia Romero)
#       2019  Tsinghua University (Author: Zhiyuan Tang)
# Apache 2.0.

# This script extracts embeddings (called "xvectors" here) from a set of
# utterances, given features and a trained DNN.  The purpose of this script
# is analogous to sid/extract_ivectors.sh: it creates archives of
# vectors that are used in speaker recognition.  Like ivectors, xvectors can
# be used in PLDA or a similar backend for scoring.

# Begin configuration section.
nj=30
cmd="run.pl"

cache_capacity=64 # Cache capacity for x-vector extractor
chunk_size=-1     # The chunk size over which the embedding is extracted.
  # If left unspecified, it uses the max_chunk_size in the nnet
                    # directory.
use_gpu=false
stage=0
echo "$0 $@"  # Print the command line for logging

if [ -f path.sh ]; then . ./path.sh; fi
. parse_options.sh || exit 1;

if [ $# != 3 ]; then
    echo "Usage: $0 <nnet-dir> <data> <xvector-dir>"
    echo " e.g.: $0 exp/xvector_nnet data/train exp/xvectors_train"
    echo "main options (for others, see top of script file)"
    echo "  --config <config-file>           # config containing options"
    echo "  --cmd (utils/run.pl|utils/queue.pl <queue opts>) # how to run jobs."
    echo "  --use-gpu <bool|false>           # If true, use GPU."
    echo "  --nj <n|30>                      # Number of jobs"
    echo "  --stage <stage|0>                # To control partial reruns"
    echo "  --cache-capacity <n|64>          # To speed-up xvector extraction"
    echo "  --chunk-size <n|-1>              # If provided, extracts embeddings with specified"
    echo "                                   # chunk size, and averages to produce final embedding"
fi

srcdir=$1
data=$2
dir=$3

for f in $srcdir/final.raw $srcdir/min_chunk_size $srcdir/max_chunk_size $data/feats.scp $data/vad.scp ; do
    [ ! -f $f ] && echo "No such file $f" && exit 1;
                     
done


min_chunk_size=`cat $srcdir/min_chunk_size 2>/dev/null`

max_chunk_size=`cat $srcdir/max_chunk_size 2>/dev/null`


nnet=$srcdir/final.raw                      #if [ -f $srcdir/extract.config ] ; then
                                            #  echo "$0: using $srcdir/extract.config to extract xvectors"
                                            #  nnet="nnet3-copy --nnet-config=$srcdir/extract.config $srcdir/final.raw - |"
                                            #fi

                      
if [ $chunk_size -le 0 ]; then
                      

    chunk_size=$max_chunk_size

fi


if [ $max_chunk_size -lt $chunk_size ]; then

    echo "$0: specified chunk size of $chunk_size is larger than the maximum chunk size, $max_chunk_size" && exit 1;

fi
  
mkdir -p $dir/log

utils/split_data.sh $data $nj


echo "$0: extracting xvectors for $data"

sdata=$data/split$nj/JOB


# Set up the features

feat="ark:apply-cmvn-sliding --norm-vars=false --center=true --cmn-window=300 scp:${sdata}/feats.scp ark:- | select-voiced-frames ark:- scp,s,cs:${sdata}/vad.scp ark:- |"


if [ $stage -le 0 ]; then

    echo "$0: extracting xvectors from nnet"

    if $use_gpu; then

        for g in $(seq $nj); do

            $cmd --gpu 1 ${dir}/log/extract.$g.log \

                nnet3-xvector-compute --use-gpu=yes --min-chunk-size=$min_chunk_size --chunk-size=$chunk_size --cache-capacity=${cache_capacity} \

                "$nnet" "`echo $feat | sed s/JOB/$g/g`" ark,scp:${dir}/xvector.$g.ark,${dir}/xvector.$g.scp || exit 1 &

            done


            
            wait

        else

            $cmd JOB=1:$nj ${dir}/log/extract.JOB.log \
                nnet3-xvector-compute --use-gpu=no --min-chunk-size=$min_chunk_size --chunk-size=$chunk_size --cache-capacity=${cache_capacity} \
                "$nnet" "$feat" ark,scp:${dir}/xvector.JOB.ark,${dir}/xvector.JOB.scp || exit 1;

            fi

        fi


        if [ $stage -le 1 ]; then

            echo "$0: combining xvectors across jobs"

            for j in $(seq $nj); do cat $dir/xvector.$j.scp; done >$dir/output.scp || exit 1;

                copy-vector scp:$dir/output.scp ark,t:$dir/output.ark.utt

            fi


            
            if [ $stage -le 2 ]; then

                echo "$0: convert output to LRE matrix scores"

                lang_names=`cat $srcdir/lang2lang_id | awk '{print $1}' | sed ':a;N;$!ba;s/\n/ /g'`

                lang_names="\ \ \ \ "$lang_names

                sed -i 's/\[//g;s/\]//g' $dir/output.ark.utt
                sed -i "1i$lang_names" $dir/output.ark.utt

                echo "Frame and utt level matrix scores prepared."

            fi
