import os
import sys
import yaml

import dask
import dask.array as da
import tifffile

if __name__ == '__main__':
    # parse config
    config_filepath = sys.argv[1]
    with open(config_filepath, 'r') as f:
        config = yaml.load(f, Loader=yaml.Loader)

    in_filepath = config['in_filepath']
    out_filepath = config['out_filepath']
    chunk_size = config['chunk_size']
    channel_names = config['channel_names']
    overwrite = config['overwrite']

    # get metadata
    with tifffile.TiffFile(in_filepath) as tif:
        pg = tif.series[0].pages[0]
        dtype, shape = pg.dtype, pg.shape

    if not isinstance(channel_names, list):
        with open(channel_names, 'r') as f:
            channel_names = [line.strip() for line in f]

    # loader function
    def load(ch):
        with tifffile.TiffFile(in_filepath) as tif:
            return tif.series[0].pages[ch].asarray()

    # load
    arr_dict = {}
    for i, c in enumerate(channel_names):
        arr = da.from_delayed(dask.delayed(load)(i), shape=shape, dtype=dtype)
        arr_dict[c] = arr.rechunk(chunk_size)

    # save
    if overwrite and os.path.isfile(out_filepath):
        os.remove(out_filepath)
    da.to_hdf5(out_filepath, arr_dict)
