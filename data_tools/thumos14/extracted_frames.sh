#! /usr/bin/bash env

cd ../
#提取光流
python build_rawframes.py ../data/thumos14/videos_val/ ../data/thumos14/rawframes/ --level 1 --flow_type tvl1 --ext mp4
echo "Raw frames (RGB and tv-l1) Generated for val set"

python build_rawframes.py ../data/thumos14/videos_test/ ../data/thumos14/rawframes/ --level 1 --flow_type tvl1 --ext mp4
echo "Raw frames (RGB and tv-l1) Generated for test set"
#提取帧图像
python build_rawframes.py ../data/thumos14/videos_val/ ../data/thumos14/rawframes/ --level 1 --flow_type None --ext mp4
echo "Raw frames (RGB and tv-l1) Generated for val set"

python build_rawframes.py ../data/thumos14/videos_test/ ../data/thumos14/rawframes/ --level 1 --flow_type None --ext mp4
echo "Raw frames (RGB and tv-l1) Generated for test set"

cd thumos14/
