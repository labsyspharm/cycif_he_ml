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

echo "run registration"
python "$CODE_DIRPATH/se_fit.py"\
    --fixed_filepath $CYCIF_TIFF_FILEPATH\
    --moving_filepath $HE_TIFF_FILEPATH\
    --nres 4\
    --niter 1000
