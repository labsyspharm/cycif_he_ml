#!/bin/bash

# paths
export HE_OMETIF_FILEPATH="$1"
export CYCIF_OMETIF_FILEPATH="$2"
export CYCIF_MARKER_FILEPATH="$3"
export PYRAMID_FILEPATH="$4"
export WORK_DIRPATH="$5"

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

# convert TIFF to HDF5
python tiff2hdf5.py\
    --in_filepath $CYCIF_OMETIF_FILEPATH\
    --out_filepath $CYCIF_H5_FILEPATH\
    --chunk_size $CHUNKSIZE\
    --channel_names $CYCIF_MARKER_FILEPATH\
    --overwrite "True"

python tiff2hdf5.py\
    --in_filepath $HE_OMETIF_FILEPATH\
    --out_filepath $HE_RGB_H5_FILEPATH\
    --chunk_size $CHUNKSIZE\
    --channel_names "r,g,b"\
    --overwrite "True"

# convert H&E from RGB to gray-scale
python rgb2gray.py\
    --in_filepath $HE_RGB_H5_FILEPATH\
    --out_filepath $HE_GRAY_H5_FILEPATH\
    --channel_names "r,g,b"\
    --dtype $FINAL_DTYPE\
    --overwrite "True"

# convert images
python se_prep.py\
    --in_filepath $CYCIF_H5_FILEPATH\
    --out_filepath $CYCIF_TIFF_FILEPATH\
    --channel_names $CYCIF_AF_CHANNELS\
    --flip "False"\
    --overwrite "True"

python se_prep.py\
    --in_filepath $HE_H5_FILEPATH\
    --out_filepath $HE_TIFF_FILEPATH\
    --channel_names "[gray]"\
    --flip "True"\
    --overwrite "True"

# run registration
python se_fit.py\
    --fixed_filepath $CYCIF_TIFF_FILEPATH\
    --moving_filepath $HE_TIFF_FILEPATH\
    --nres 4\
    --niter 1000

# transform images in batch
for CHANNEL_NAME in "r g b"
do
    python se_prep.py\
        --in_filepath $HE_H5_FILEPATH\
        --out_filepath $TMP_TIFF_FILEPATH\
        --channel_names "[$CHANNEL_NAME]"\
        --flip "False"\
        --overwrite "True"
    python se_transform.py\
        --param_filepath $PARAM_FILEPATH\
        --moving_filepath $TMP_TIFF_FILEPATH\
        --out_filepath $TMP_TIFF_FILEPATH
    python se_postprocessing.py\
        --in_filepath $TMP_TIFF_FILEPATH\
        --out_filepath "$WORK_DIRPATH/HE_$CHANNEL_NAME.tif"\
        --dtype $FINAL_DTYPE
done

# generate pyramid
PYRAMID_ORDER=()
cat $CYCIF_MARKER_FILEPATH | while read LINE
do
    # save CyCIF images to individual TIFF
    python se_prep.py\
        --in_filepath $CYCIF_H5_FILEPATH\
        --out_filepath "$WORK_DIRPATH/CYCIF_$LINE.tif"\
        --channel_names "[$LINE]"\
        --flip "False"\
        --overwrite "True"
    # record file list
    PYRAMID_ORDER+=("$WORK_DIRPATH/CYCIF_$LINE.tif")
done

for CHANNEL_NAME in "r g b"
do
    # record file list
    PYRAMID_ORDER+=("$WORK_DIRPATH/HE_$CHANNEL_NAME.tif")
done

# function to join bash array
# ref: https://zaiste.net/posts/how-to-join-elements-of-array-bash/
function join { local IFS="$1"; shift; echo "$*"; }

# run pyramid generation
python make_pyramid.py\
    --in_filepaths $(join , ${PYRAMID_ORDER[@]})\
    --out_filepath $PYRAMID_FILEPATH\
    --tile_size 1024\
