#!/bin/bash


# load config
CONFIG_FILEPATH="$1"
source $CONFIG_FILEPATH


echo "run registration"
python "$CODE_DIRPATH/se_fit.py"\
    --fixed_filepath $CYCIF_TIFF_FILEPATH\
    --moving_filepath $HE_TIFF_FILEPATH\
    --out_filepath $TMP_FILEPATH\
    --nres $AFFINE_NRES\
    --niter $AFFINE_NITER
mv "./TransformParameters.0.txt" $PARAM_FILEPATH


echo "post-processing registration preview"
python "$CODE_DIRPATH/se_preprocessing.py"\
    --in_filepath $TMP_FILEPATH\
    --out_filepath $TMP_FILEPATH\
    --dtype "uint16"


echo "construct pyramid for preview on OMERO server"
echo "$TMP_FILEPATH" > $TMP_FILELIST_FILEPATH
python "$CODE_DIRPATH/make_pyramid.py"\
    --filelist_filepath $TMP_FILELIST_FILEPATH\
    --out_filepath $VIS_REG_FILEPATH\
    --tile_size $PYRAMID_TILE_SIZE
echo "preview of registration result available at:"
echo $VIZ_REG_FILEPATH
