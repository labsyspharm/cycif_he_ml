import os
import typing

import fire
import h5py
import numpy as np
import dask.array as da

from skimage import color, util


def rgb2gray(
    in_filepath: str,
    out_filepath: str,
    channel_names: typing.List[str],
    dtype: str = "float64",
    overwrite: bool = False,
):
    """
    Convert RGB image in HDF5 format to gray-scale.

    Args:
        in_filepath, out_filepath: str
            Paths of input and output HDF5 files.
        channel_names: list(str)
            Names of the channels in order of red, green, and blue.
        dtype: str [optional]
            Image data type conversion. Default is skimage.rgb2gray output
            (float64, range [0, 1]). Accepted formats are bool, uint8, int16,
            uint16, float32, float64.
        overwrite: bool [optional]
            Overwrite the output file if already exists, default False.
    """
    # check dtype argument
    if dtype == "bool":
        cast_fn = util.img_as_bool
    elif dtype == "uint8":
        cast_fn = util.img_as_ubyte
    elif dtype == "int16":
        cast_fn = util.img_as_int
    elif dtype == "uint16":
        cast_fn = util.img_as_uint
    elif dtype == "float32":
        cast_fn = util.img_as_float32
    elif dtype == "float64":
        cast_fn = util.img_as_float64
    else:
        raise NotImplementedError(
            "dtype {} not recognized. Currently accepted"
            "formats are bool, uint8, int16, uint16, float32, float64."
            .format(dtype)
        )

    # load data as dask array
    f = h5py.File(in_filepath, "r")
    arr_list = [da.from_array(f[ch]) for ch in channel_names[:3]]

    # convert blockwise
    def fn(r, g, b):
        rgb = np.stack([r, g, b], axis=-1)
        gray = color.rgb2gray(rgb)
        gray = cast_fn(gray)
        return gray

    gray_img = da.map_blocks(fn, *arr_list, dtype=dtype,
                             chunks=arr_list[0].chunks)

    # save to disk
    if overwrite and os.path.isfile(out_filepath):
        os.remove(out_filepath)
    da.to_hdf5(out_filepath, "/gray", gray_img)


if __name__ == "__main__":
    fire.Fire(rgb2gray)
