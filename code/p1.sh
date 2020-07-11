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

echo "convert TIFF to HDF5"
python "$CODE_DIRPATH/tiff2hdf5.py"\
    --in_filepath $CYCIF_OMETIF_FILEPATH\
    --out_filepath $CYCIF_H5_FILEPATH\
    --chunk_size $CHUNKSIZE\
    --channel_names $CYCIF_MARKER_FILEPATH\
    --overwrite "True"

python "$CODE_DIRPATH/tiff2hdf5.py"\
    --in_filepath $HE_OMETIF_FILEPATH\
    --out_filepath $HE_RGB_H5_FILEPATH\
    --chunk_size $CHUNKSIZE\
    --channel_names "r,g,b"\
    --overwrite "True"

echo "convert H&E from RGB to gray-scale"
python "$CODE_DIRPATH/rgb2gray.py"\
    --in_filepath $HE_RGB_H5_FILEPATH\
    --out_filepath $HE_GRAY_H5_FILEPATH\
    --channel_names "r,g,b"\
    --dtype $FINAL_DTYPE\
    --overwrite "True"

echo "convert images"
python "$CODE_DIRPATH/se_prep.py"\
    --in_filepath $CYCIF_H5_FILEPATH\
    --out_filepath $CYCIF_TIFF_FILEPATH\
    --channel_names $CYCIF_AF_CHANNELS\
    --flip "False"\
    --overwrite "True"

python "$CODE_DIRPATH/se_prep.py"\
    --in_filepath $HE_GRAY_H5_FILEPATH\
    --out_filepath $HE_TIFF_FILEPATH\
    --channel_names "[gray,]"\
    --flip "True"\
    --overwrite "True"
