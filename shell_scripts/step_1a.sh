#!/bin/bash


# load config
CONFIG_FILEPATH="$1"
source $CONFIG_FILEPATH


echo "convert TIFF to HDF5"
python "$CODE_DIRPATH/tiff2hdf5.py"\
    --in_filepath $CYCIF_OMETIF_FILEPATH\
    --out_filepath $CYCIF_H5_FILEPATH\
    --chunk_size $CHUNKSIZE\
    --channel_names $CYCIF_MARKER_FILEPATH\
    --overwrite "True"
python "$CODE_DIRPATH/tiff2hdf5.py"\
    --in_filepath $HE_OMETIF_FILEPATH\
    --out_filepath $TMP_H5_FILEPATH\
    --chunk_size $CHUNKSIZE\
    --channel_names "r,g,b"\
    --overwrite "True"

echo "downscale H&E for TNP project"
python "$CODE_DIRPATH/downscale.py"\
    --in_filepath $TMP_H5_FILEPATH\
    --out_filepath $HE_RGB_H5_FILEPATH\
    --factors "(2,2)"\
    --chunk_size $CHUNKSIZE\
    --overwrite "True"
