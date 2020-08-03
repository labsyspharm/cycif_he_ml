#!/bin/bash


# load config
CONFIG_FILEPATH="$1"
source $CONFIG_FILEPATH


echo "transform images according to fitted transformation"
for CHANNEL_NAME in "${RGB[@]}"
do
    python "$CODE_DIRPATH/se_prep.py"\
        --in_filepath $HE_RGB_H5_FILEPATH\
        --out_filepath $TMP_TIFF_FILEPATH\
        --channel_names "[$CHANNEL_NAME]"\
        --flip "False"\
        --overwrite "True"
    python "$CODE_DIRPATH/transform_by_anchor.py"\
        --template_filepath $CYCIF_TIFF_FILEPATH\
        --src_filepath $TMP_TIFF_FILEPATH\
        --anchor_filepath $ANCHOR_FILEPATH\
        --out_filepath $TMP_FILEPATH\
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


echo "unbundle CyCIF images"
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


echo "prepare file list"
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
sed -i '1d' $FILELIST_FILEPATH


echo "run pyramid generation"
python "${CODE_DIRPATH}/make_pyramid.py"\
    --filelist_filepath $FILELIST_FILEPATH\
    --out_filepath $PYRAMID_FILEPATH\
    --tile_size $PYRAMID_TILE_SIZE
echo "final result available at:"
echo $PYRAMID_FILEPATH
