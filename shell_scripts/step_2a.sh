#!/bin/bash


# load config
CONFIG_FILEPATH="$1"
source $CONFIG_FILEPATH


echo "run registration"
python "$CODE_DIRPATH/se_fit.py"\
    --fixed_filepath $CYCIF_TIFF_FILEPATH\
    --moving_filepath $HE_TIFF_FILEPATH\
    --out_filepath $TMP_TIFF_FILEPATH\
    --nres $AFFINE_NRES\
    --niter $AFFINE_NITER
mv "./TransformParameters.0.txt" $PARAM_FILEPATH
