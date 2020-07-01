import os
import sys
import yaml

import numpy as np
import h5py
import dask
import dask.array as da

from skimage.morphology import disk
#from skimage.feature import match_template
from template import match_template

if __name__ == '__main__':
    # parse config
    config_filepath = sys.argv[1]
    with open(config_filepath, 'r') as f:
        config = yaml.load(f, Loader=yaml.Loader)

    in1_filepath = config['in1_filepath']
    in1_name = config['in1_name']
    in1_chunk_size = config['in1_chunk_size']
    in2_filepath = config['in2_filepath']
    in2_name = config['in2_name']
    in2_chunk_size = config['in2_chunk_size']
    out_filepath = config['out_filepath']
    overwrite = config['overwrite']

    # load data
    f1 = h5py.File(in1_filepath, 'r')[in1_name]
    f2 = h5py.File(in2_filepath, 'r')[in2_name]
    arr1 = da.from_array(f1, chunks=in1_chunk_size)
    arr2 = da.from_array(f2, chunks=in2_chunk_size)

    # define match function
    selem = arr1[0:in1_chunk_size[0], 0:in1_chunk_size[1]]
    match_fn = lambda b: match_template(
            image=b,
            template=selem,
            pad_input=True,
            )

    # map function across overlapping chunks
    overlap_depth = {0: selem.shape[0]//2, 1: selem.shape[1]//2}
    boundary = {0: 0, 1: 0}
    res = arr2.map_overlap(match_fn,
            depth=overlap_depth, boundary=boundary,
            dtype=float, trim=True)

    # save to disk
    if overwrite and os.path.isfile(out_filepath):
        os.remove(out_filepath)
    da.to_hdf5(out_filepath, '/response', res)
