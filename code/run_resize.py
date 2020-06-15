import dask
import dask.array as da
import dask.distributed as dd

from dask_image import imread
from skimage import transform

def myfunc(x):
    return transform.rescale(x, (13560, 13070), preserve_range=True)\
            .astype('uint8')

if __name__ == '__main__':
    # create local cluster
    client = dd.Client(n_workers=4)

    # path
    filepath = './he_img.tif'

    # load data
    a = imread.imread(filepath)\
            [0, 0, ...]\
            .rechunk((32, 32))
    print('='*20)
    print(a)
    print('='*20)

    # assemble pipeline
    b = da.from_delayed(dask.delayed(myfunc)(a),
            shape=(13560, 13070), dtype='uint8')

    # compute
    b.compute()

    # check result
    print('='*20)
    print(b)
    print('='*20)
