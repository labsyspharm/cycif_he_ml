#!/bin/bash

# paths
export HE_OMETIF_FILEPATH="$1"
export CYCIF_OMETIF_FILEPATH="$2"
export CYCIF_MARKER_FILEPATH="$3"
export PYRAMID_FILEPATH="$4"
export WORK_DIRPATH="$5"
export CODE_DIRPATH="$6"

# critical params
export CYCIF_AF_CHANNELS="[DNA1,bg2a,bg3a,bg4a]"

# less critical params
export CHUNKSIZE="[1000,1000]"
export FINAL_DTYPE="uint16"

# intermediate file paths
export CYCIF_H5_FILEPATH="$WORK_DIRPATH/cycif.h5"
export HE_RGB_H5_FILEPATH="$WORK_DIRPATH/he_rgb.h5"
export HE_GRAY_H5_FILEPATH="$WORK_DIRPATH/he_gray.h5"
export CYCIF_TIFF_FILEPATH="$WORK_DIRPATH/cycif.tif"
export HE_TIFF_FILEPATH="$WORK_DIRPATH/he.tif"
export TMP_TIFF_FILEPATH="$WORK_DIRPATH/tmp.tif"
export PARAM_FILEPATH="$WORK_DIRPATH/TransformParameters.0.txt"
export FILELIST_FILEPATH="$WORK_DIRPATH/filelist.txt"

echo "transform images in batch"
RGB=(r g b)
for CHANNEL_NAME in "${RGB[@]}"
do
    python "$CODE_DIRPATH/se_prep.py"\
        --in_filepath $HE_RGB_H5_FILEPATH\
        --out_filepath $TMP_TIFF_FILEPATH\
        --channel_names "[$CHANNEL_NAME]"\
        --flip "False"\
        --overwrite "True"
    python "$CODE_DIRPATH/se_transform.py"\
        --param_filepath $PARAM_FILEPATH\
        --moving_filepath $TMP_TIFF_FILEPATH\
        --out_filepath $TMP_TIFF_FILEPATH
    python "$CODE_DIRPATH/se_postprocessing.py"\
        --in_filepath $TMP_TIFF_FILEPATH\
        --out_filepath "$WORK_DIRPATH/HE_${CHANNEL_NAME}.tif"\
        --dtype $FINAL_DTYPE
done

echo "generate pyramid"
cat $CYCIF_MARKER_FILEPATH | while read LINE
do
    # save CyCIF images to individual TIFF
    python "$CODE_DIRPATH/se_prep.py"\
        --in_filepath $CYCIF_H5_FILEPATH\
        --out_filepath "$WORK_DIRPATH/CYCIF_${LINE}.tif"\
        --channel_names "[$LINE]"\
        --flip "False"\
        --overwrite "True"
done

echo "" > $FILELIST_FILEPATH

cat $CYCIF_MARKER_FILEPATH | while read LINE
do
    # record file list
    echo "$WORK_DIRPATH/CYCIF_${LINE}.tif" >> $FILELIST_FILEPATH
done


for CHANNEL_NAME in "${RGB[@]}"
do
    # record file list
    echo "$WORK_DIRPATH/HE_${CHANNEL_NAME}.tif" >> $FILELIST_FILEPATH
done

echo "run pyramid generation"
python "$CODE_DIRPATH/make_pyramid.py"\
    --in_filepaths $(cat $FILELIST_FILEPATH | sed "1d" | paste -sd ',')\
    --out_filepath $PYRAMID_FILEPATH\
    --tile_size 1024\
