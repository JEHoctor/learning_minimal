#! /usr/bin/bash
set -euf

mkdir data
cd data

for SPLIT in training test
do
	SPLIT_FULL_NAME="multi_view_${SPLIT}_dslr_undistorted"
	SPLIT_7Z_FILE_NAME="${SPLIT_FULL_NAME}.7z"
	wget "https://www.eth3d.net/data/${SPLIT_FULL_NAME}.7z"
	mkdir $SPLIT_FULL_NAME
	cd $SPLIT_FULL_NAME
	7z x "../${SPLIT_7Z_FILE_NAME}"
	cd ..
	rm $SPLIT_7Z_FILE_NAME
done
