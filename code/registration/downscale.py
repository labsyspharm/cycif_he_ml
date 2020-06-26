import os
import sys
import yaml

import h5py
import dask.array as da
from skimage import transform

if __name__ == '__main__':
    # parse config
    config_filepath = sys.argv[1]
    with open(config_filepath, 'r') as f:
        config = yaml.load(f, Loader=yaml.Loader)

    in_filepath = config['in_filepath']
    out_filepath = config['out_filepath']
    chunk_size = tuple(config['chunk_size'])
    factors = tuple(config['factors'])
    overwrite = config['overwrite']

    # convert blockwise
    def downscale(b):
        return transform.downscale_local_mean(b, factors).astype(b.dtype)

    # save to disk
    if overwrite and os.path.isfile(out_filepath):
        os.remove(out_filepath)

    # load data
    f_in = h5py.File(in_filepath, 'r')
    f_out = h5py.File(out_filepath, 'w')

    for name in f_in.keys():
        arr_in = da.from_array(f_in[name], chunks=chunk_size)
        arr_out = da.map_blocks(downscale, arr_in, dtype=arr_in.dtype)
        arr_out.compute_chunk_sizes()
        d_out = f_out.create_dataset(name, shape=arr_out.shape,
                chunks=chunk_size, dtype=arr_out.dtype)
        da.store(arr_out, d_out)
