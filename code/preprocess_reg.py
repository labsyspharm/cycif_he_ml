import os
import tifffile
from skimage import io, transform, img_as_uint

if __name__ == '__main__':
    # paths
    data_folderpath = os.path.expanduser('../data')
    dna1_filepath = os.path.join(data_folderpath, 'cycif_dna1.tif')
    he_filepath = os.path.join(data_folderpath, 'he_img.tif')

    # load data and preprocessing
    dna1 = io.imread(dna1_filepath)
    dna1 = dna1[:dna1.shape[0]//2, :dna1.shape[1]//2]
    dna1 = img_as_uint(dna1)
    io.imsave('../data/dna1_small.tif', dna1)

    with tifffile.TiffFile(he_filepath) as tif:
        he = tif.asarray()[0, ...] # red channel
    he = he[:he.shape[0]//2, :he.shape[1]//2]
    he = transform.downscale_local_mean(he, factors=(2,2))\
            .astype(he.dtype)
    he = img_as_uint(he)
    io.imsave('../data/he_small.tif', he)

    he_inv = 255-he
    io.imsave('../data/he_small_inv.tif', he_inv)
