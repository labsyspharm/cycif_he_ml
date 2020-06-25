import os
import sys
import yaml

import numpy as np
import h5py
import dask.array as da
from skimage import color, img_as_ubyte

if __name__ == '__main__':
    # parse config
    config_filepath = sys.argv[1]
    with open(config_filepath, 'r') as f:
        config = yaml.load(f, Loader=yaml.Loader)

    in_filepath = config['in_filepath']
    out_filepath = config['out_filepath']
    chunk_size = config['chunk_size']
    rgb_names = config['rgb_names']
    overwrite = config['overwrite']

    # load data
    f = h5py.File(in_filepath, 'r')
    arr_list = [da.from_array(f[ch], chunks=chunk_size) for ch in rgb_names]

    # convert blockwise
    def rgb2gray(r, g, b):
        rgb = np.stack([r, g, b], axis=-1)
        return img_as_ubyte(color.rgb2gray(rgb))
    gray_img = da.map_blocks(rgb2gray, *arr_list, dtype=np.uint8,
            chunks=arr_list[0].chunks)

    # save to disk
    if overwrite and os.path.isfile(out_filepath):
        os.remove(out_filepath)
    da.to_hdf5(out_filepath, '/gray', gray_img)
