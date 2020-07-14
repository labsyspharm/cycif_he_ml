import os
import typing

import h5py
import dask.array as da
import fire

from skimage import transform


def downscale(in_filepath: str, out_filepath: str,
        factors: typing.Tuple[int, int],
        chunk_size: typing.Tuple[int, int]=None, overwrite: bool=False):
    '''
    Downscale image in HDF5 format using skimage.transform.downscale_local_mean
    function and dask parallelization.

    Args:
        in_filepath, out_filepath: str
            Paths of input and output HDF5 files.
        factors: tuple(int, int)
            Downscale factors.
        chunk_size: tuple(int, int) [optional]
            Chunk size of the HDF5 file. If None (default), no chunking.
        overwrite: bool [optional]
            Overwrite the output file if already exists, default False.
    '''
    # check overwrite
    if overwrite and os.path.isfile(out_filepath):
        os.remove(out_filepath)

    # load data
    f_in = h5py.File(in_filepath, 'r')
    f_out = h5py.File(out_filepath, 'w')

    # convert blockwise
    def fn(b):
        return transform.downscale_local_mean(b, factors).astype(b.dtype)

    for name in f_in.keys():
        arr_in = da.from_array(f_in[name])
        arr_out = da.map_blocks(downscale, arr_in, dtype=arr_in.dtype)
        arr_out.compute_chunk_sizes()
        d_out = f_out.create_dataset(name, shape=arr_out.shape,
                chunks=chunk_size, dtype=arr_out.dtype)
        da.store(arr_out, d_out)


if __name__ == '__main__':
    fire.Fire(downscale)
