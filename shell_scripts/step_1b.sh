#!/bin/bash


# load config
CONFIG_FILEPATH="$1"
source $CONFIG_FILEPATH


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
    --out_filepath $TMP_TIFF_FILEPATH\
    --channel_names "[gray,]"\
    --flip "True"\
    --overwrite "True"

echo "transform by anchor"
python "$CODE_DIRPATH/transform_by_anchor.py"\
    --src_filepath $HE_TIFF_FILEPATH\
    --anchor_filepath $ANCHOR_FILEPATH\
    --out_filepath $HE_TIFF_FILEPATH\
    --overwrite "True"
