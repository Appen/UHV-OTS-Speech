#!/bin/bash
# This script will download VoxCeleb1 dataset into /data/ folder

echo "Creating /data/VoxCeleb/VoxCeleb1 folder"
[ ! -d "/data" ] && mkdir -p /data
[ ! -d "/data/VoxCeleb" ] && mkdir -p /data/VoxCeleb 
[ ! -d "/data/VoxCeleb/VoxCeleb1" ] && mkdir -p /data/VoxCeleb/VoxCeleb1 


echo "downloading VoxCeleb 1 datasets in to /data/VoxCeleb/VoxCeleb1"
for i in a b c d; do
    wget -P /data/VoxCeleb/VoxCeleb1 -c https://thor.robots.ox.ac.uk/~vgg/data/voxceleb/vox1a/vox1_dev_wav_parta${i} --user voxceleb1912 --password 0s42xuw6: 
    sleep 60
done

#wait
echo "VoxCeleb 1 downlaoding is done"
