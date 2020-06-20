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

    with tifffile.TiffFile('../data/DNA6.tif') as tif:
        dna6 = tif.series[0].pages[0].asarray()
        dna6 = transform.downscale_local_mean(dna6, (2, 2))\
                .astype(dna6.dtype)
        dna6 = img_as_ubyte(dna6)

    with tifffile.TiffFile('../data/CD20.tif') as tif:
        cd20 = tif.series[0].pages[0].asarray()
        cd20 = transform.downscale_local_mean(cd20, (2, 2))\
                .astype(cd20.dtype)
        cd20 = img_as_ubyte(cd20)

    with tifffile.TiffFile('../data/he_img.tif') as tif:
        he = None
        for i in range(3):
            he_i = tif.series[0].pages[0].asarray()[i, ...]
            he_i = transform.downscale_local_mean(he_i, (4, 4))\
                    .astype('uint8')
            if he is None:
                he = np.zeros(he_i.shape+(3,), dtype=he_i.dtype)
            he[..., i] = he_i
        he = color.rgb2gray(he)
        he = img_as_ubyte(he)
        he = 255-he

    # transform H&E
    trans = transform.AffineTransform(rotation=np.radians(-5))
    he = transform.warp(he, inverse_map=trans.inverse)
    trans = transform.AffineTransform(translation=(-800, 200))
    he = transform.warp(he, inverse_map=trans.inverse)
    he = img_as_ubyte(he)

    same_shape = (min(he.shape[0], dna1.shape[0]),
            min(he.shape[1], dna1.shape[1]))
    he = he[:same_shape[0], :same_shape[1]]
    dna1 = dna1[:same_shape[0], :same_shape[1]]
    dna6 = dna6[:same_shape[0], :same_shape[1]]
    cd20 = cd20[:same_shape[0], :same_shape[1]]

    he = transform.rotate(he, angle=3, center=(0, he.shape[1]),
            preserve_range=True).astype('uint8')

    trans = transform.AffineTransform(translation=(0, 700))
    he = transform.warp(he, inverse_map=trans.inverse)
    he = img_as_ubyte(he)

    io.imsave('../data/aligned_DNA1.tif', dna1)
    io.imsave('../data/aligned_DNA6.tif', dna6)
    io.imsave('../data/aligned_CD20.tif', cd20)
    io.imsave('../data/aligned_he.tif', he)

    with napari.gui_qt():
        viewer = napari.viewer.Viewer(show=False)
        viewer.add_image(dna1, name='dna1', colormap='green',
                blending='additive')
        viewer.add_image(dna6, name='dna6', colormap='green',
                blending='additive')
        viewer.add_image(cd20, name='cd20', colormap='green',
                blending='additive')
        viewer.add_image(he, name='he', colormap='red',
                blending='additive')
        viewer.show()
