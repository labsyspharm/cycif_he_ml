import getpass

import fsspec
import dask
import dask.array as da

from skimage.external import tifffile

def get_top_series(path):
    with fs.open(path, mode='rb') as f:
        with tifffile.TiffFile(f) as tif:
            return tif.series[0].asarray(memmap=True)

fs = fsspec.filesystem('sftp', host='transfer.rc.hms.harvard.edu', port=22,
        username=getpass.getpass(prompt='Username:'),
        password=getpass.getpass(prompt='Password:'),
        )
path = 'sftp://transfer.rc.hms.harvard.edu'\
        '/n/files/ImStor/sorger/data/hungyiwu'\
        '/dataset/pca_z170/roi_ometif/Z170_1_0.ome.tif'

array = get_top_series(path)
print(array.shape)

lazy_array = dask.delayed(get_top_series)(path)
dask_array = da.from_delayed(lazy_array, shape=array.shape, dtype=array.dtype)
print(dask_array.shape)
