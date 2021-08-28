#!/bin/bash

WAV_DIR=$1
SEG_DIR=$2

exp_dir='exp_ots'

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
WEIGHTS=$DIR/VBx/models/ResNet152_16kHz/nnet/raw_58.pth
BACKEND_DIR=$DIR/VBx/models/ResNet152_16kHz

EXTRACT_SCRIPT=$DIR/VBx/extract.sh
DEVICE=0

vad_dir=$SEG_DIR
xvec_dir=$exp_dir/energy_VAD/xvectors

mkdir -p $xvec_dir






