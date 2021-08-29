#!/bin/bash

feat_paraller_file='feat_papralle.lst'
feat_out_file='feat_new.txt'

lines=`cat $feat_paraller_file`
while read -r line; do
    ID=`echo $line | awk '{print $2}'`
    feat_1st=`echo $line | awk '{print $3}'`
    feat_2nd=`echo $line | awk '{print $4}'`
    echo "$ID [" >> $feat_out_file
    concat-feats --binary=false $feat_1st $feat_2nd - | tail -n +2 >> $feat_out_file


done < "$feat_paraller_file"
