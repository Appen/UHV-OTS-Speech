#!/bin/bash

. ./path.sh
train_embeddings=embeddings/embedding_obj_train_gender_voxceleb1_ots_asr001_asr003_voxceleb2_shuf_300000.pkl
test_embeddings=embeddings/embedding_obj_test_gender_voxceleb1.pkl
classifier_model=model/classifier_gender_300000.pkl
if [ ! -f "$classifier_model" ]; then
    echo "$classifier_model does not exist."
    #python3 gedetec_s4_compute_embedding.py hparams/gedetec_s4_compute_embedding_pretrain.yaml 
    python3 utils/gedetec_s5_train_mlp_gender_2.py  
fi

python3 utils/gedetec_s6_test_mlp_gender_2.py $classifier_model $test_embeddings
