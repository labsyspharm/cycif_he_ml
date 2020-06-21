import numpy as np
import napari
import napari.viewer as nv
import tifffile

from skimage import io, color, transform, img_as_ubyte

if __name__ == '__main__':
    with tifffile.TiffFile('../data/DNA1.tif') as tif:
        dna1 = tif.series[0].pages[0].asarray()
        dna1 = transform.downscale_local_mean(dna1, (2, 2))\
                .astype(dna1.dtype)
        dna1 = img_as_ubyte(dna1)

    with tifffile.TiffFile('../data/he_img.tif') as tif:
        he = None
        for i in range(3):
            he_i = tif.series[0].pages[0].asarray()[i, ...]
            he_i = transform.downscale_local_mean(he_i, (4, 4))\
                    .astype('uint8')
            if he is None:
                he = np.zeros(he_i.shape+(3,), dtype=he_i.dtype)
            he[..., i] = he_i

    print('data loaded')

    # transform H&E
    trans = transform.AffineTransform(rotation=np.radians(-5))
    he = transform.warp(he, inverse_map=trans.inverse)
    trans = transform.AffineTransform(translation=(-800, 200))
    he = transform.warp(he, inverse_map=trans.inverse)
    he = img_as_ubyte(he)

    print('first transform done')

    same_shape = (min(he.shape[0], dna1.shape[0]),
            min(he.shape[1], dna1.shape[1]))
    he = he[:same_shape[0], :same_shape[1]]

    print('truncate done')

    he = transform.rotate(he, angle=3, center=(0, he.shape[1]),
            preserve_range=True).astype('uint8')

    trans = transform.AffineTransform(translation=(0, 700))
    he = transform.warp(he, inverse_map=trans.inverse)
    he = img_as_ubyte(he)

    print('second transform done')

    io.imsave('../data/aligned_he_rgb.tif', he)
