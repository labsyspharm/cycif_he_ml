import typing

import fire
import h5py
import tifffile
import numpy as np
import dask.array as da


def maxproj2tiff(in_filepath: str, out_filepath: str,
        channel_names: typing.Any=None,
        flip: bool=False, overwrite: bool=False):
    '''
    Maximum projection over channels of HDF5 and save to disk as TIFF.

    Args:
        in_filepath, out_filepath: str
            Paths of input HDF5 and output TIFF files.
        channel_names: list(str), str
            Names of the HDF5 datasets to use. If string, treated as path
            to a text file where each line is the name of a channel.
        overwrite: bool [optional]
            Overwrite the output file if already exists, default False.
    '''
    # parse channel names
    if isinstance(channel_names, str):
        with open(channel_names, 'r') as f:
            channel_names = [line.strip() for line in f]

    # load data
    f = h5py.File(in_filepath, 'r')

    # allowing same API for images not need maximum projection
    # but still need to be saved as TIFF
    if len(channel_names) > 1:
        arr = f[channel_names[0]]
    else:
        arr_list = [da.from_array(f[key]) for key in channel_names]
        arr = da.max(da.stack(arr_list, axis=-1), axis=-1)

    # in case flipping is needed
    if flip:
        try:
            dtype = np.iinfo(arr.dtype)
        except:
            dtype = np.finfo(arr.dtype)
        arr = dtype.max - arr

    # save to disk as TIFF
    tifffile.imsave(out_filepath, arr)


if __name__ == '__main__':
    fire.Fire(maxproj2tiff)
