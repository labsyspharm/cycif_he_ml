#!/bin/bash


# load config
CONFIG_FILEPATH="$1"
source $CONFIG_FILEPATH


echo "post-processing registration preview"
python "$CODE_DIRPATH/se_postprocessing.py"\
    --in_filepath $TMP_TIFF_FILEPATH\
    --out_filepath $TMP_TIFF_FILEPATH\
    --dtype "uint16"


echo "construct pyramid for preview on OMERO server"
echo "$TMP_TIFF_FILEPATH" > $TMP_FILELIST_FILEPATH
python "$CODE_DIRPATH/make_pyramid.py"\
    --filelist_filepath $TMP_FILELIST_FILEPATH\
    --out_filepath $VIS_REG_FILEPATH\
    --tile_size $PYRAMID_TILE_SIZE
echo "preview of registration result available at:"
echo $VIZ_REG_FILEPATH
