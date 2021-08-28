#!/bin/bash
# This script will download VoxCeleb1 dataset into /data/ folder

echo "Creating /data/VoxConverse folder"
[ ! -d "/data" ] && mkdir -p /data
[ ! -d "/data/VoxConverse" ] && mkdir -p /data/VoxConverse


echo "downloading VoxConverse datasets in to /data/VoxConverse"
if [ ! -f "/data/VoxConverse/voxconverse_dev_wav.zip" ]; then
  wget -P /data/VoxConverse -c https://www.robots.ox.ac.uk/~vgg/data/voxconverse/data/voxconverse_dev_wav.zip
fi
echo "VoxConverse downloading is done"

if [ ! -d "/data/VoxConverse/audio" ]; then
 unzip /data/VoxConverse/voxconverse_dev_wav.zip -d /data/VoxConverse/
fi

if  [ ! -d "/opt/scripts/speaker_diarization/voxconverse" ]; then
 git clone https://github.com/joonson/voxconverse.git
fi


