import os
import sys
import yaml

import numpy as np
import h5py
import dask.array as da

from skimage.morphology import disk
from skimage.feature import match_template

if __name__ == '__main__':
    # parse config
    config_filepath = sys.argv[1]
    with open(config_filepath, 'r') as f:
        config = yaml.load(f, Loader=yaml.Loader)

    in1_filepath = config['in1_filepath']
    in1_name = config['in1_name']
    in2_filepath = config['in2_filepath']
    in2_name = config['in2_name']
    out_filepath = config['out_filepath']
    chunk_size = config['chunk_size']
    overwrite = config['overwrite']

    # load data
    f1 = h5py.File(in1_filepath, 'r')[in1_name]
    f2 = h5py.File(in2_filepath, 'r')[in2_name]
    arr1 = da.from_array(f1, chunks=chunk_size)
    arr2 = da.from_array(f2, chunks=chunk_size)

    # define match function
    selem = arr1[0:chunk_size[0], 0:chunk_size[1]]
    match_fn = lambda block: match_template(
            image=block,
            template=selem,
            pad_input=False,
            )

    # map function across overlapping chunks
    overlap_depth = {0: selem.shape[0]//2, 1: selem.shape[1]//2}
    boundary = {0: 0, 1: 0}
    res = arr2.map_overlap(match_fn, depth=overlap_depth, boundary=boundary,
            dtype=np.float64, trim=False, chunks=arr2.chunks)

    # save to disk
    if overwrite and os.path.isfile(out_filepath):
        os.remove(out_filepath)
    da.to_hdf5(out_filepath, '/response', res)
