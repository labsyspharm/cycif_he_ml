import numpy as np
import h5py
import dask.array as da

from skimage.morphology import disk
from skimage.feature import match_template

if __name__ == '__main__':
    # load data
    f = h5py.File('he.hdf5', 'r')['r'] # HDF5 chunk size (1000, 1000)
    chunk_size = (5000, 5000) # for dask array
    x = da.from_array(f, chunks=chunk_size)

    # define match function
    selem = disk(5)
    match_fn = lambda block: match_template(
            image=block,
            template=selem,
            pad_input=False,
            )

    # map function across overlapping chunks
    overlap_depth = {0: selem.shape[0]//2, 1: selem.shape[1]//2}
    boundary = {0: 0, 1: 0}
    res = x.map_overlap(match_fn, depth=overlap_depth, boundary=boundary,
            dtype=np.float64, trim=False, chunks=x.chunks)

    # save to disk
    da.to_hdf5('res.hdf5', '/r', res)
