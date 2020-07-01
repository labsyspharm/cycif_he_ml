import os
import typing

import dask
import dask.array as da
import tifffile
import fire


def tiff2hdf5(in_filepath: str, out_filepath: str,
        chunk_size: typing.Tuple[int, int]=None,
        channel_names: typing.Any=None, overwrite: bool=False):
    '''
    Convert multi-channel TIFF image into HDF5 file format, each channel
    as one 2D array.

    Args:
        in_filepath, out_filepath: str
            Paths of input TIFF and output HDF5 files.
        chunk_size: tuple(int, int) [optional]
            Chunk size of the HDF5 file. If None (default), no chunking.
        channel_names: list(str), str [optional]
            Names of the TIFF image channels for naming arrays in HDF5 file.
            If None (default), named as '0', '1', ..., etc. If string, treated
            as path to a text file where each line is the name of a channel.
        overwrite: bool [optional]
            Overwrite the output file if already exists, default False.
    '''
    # get metadata
    with tifffile.TiffFile(in_filepath) as tif:
        pg = tif.series[0].pages[0]
        dtype, shape = pg.dtype, pg.shape
        npg = len(tif.series[0].pages)

    # parse channel names
    if channel_names is None:
        channel_names = [str(i) for i in range(npg)]
    elif isinstance(channel_names, str):
        with open(channel_names, 'r') as f:
            channel_names = [line.strip() for line in f]

    # check channel name length
    if len(channel_names) != npg:
        raise ValueError('Got {} channel names but {} channels in {}.'
                .format(len(channel_names), npg, in_filepath))

    # loader function
    def load(ch):
        with tifffile.TiffFile(in_filepath) as tif:
            return tif.series[0].pages[ch].asarray()
    delayed_load = dask.delayed(load)

    # load as dask array
    arr_dict = {}
    for i, c in enumerate(channel_names):
        arr = da.from_delayed(delayed_load(i), shape=shape, dtype=dtype)
        if chunk_size is not None:
            arr_dict[c] = arr.rechunk(chunk_size)

    # save to disk
    if overwrite and os.path.isfile(out_filepath):
        os.remove(out_filepath)
    da.to_hdf5(out_filepath, arr_dict)


if __name__ == '__main__':
    fire.Fire(tiff2hdf5)
