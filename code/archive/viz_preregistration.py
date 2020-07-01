import numpy as np
import napari
import napari.viewer as nv
import tifffile

from skimage import io, color, transform, img_as_ubyte

if __name__ == '__main__':
    with tifffile.TiffFile('../data/DNA6.tif') as tif:
        dna6 = tif.series[0].pages[0].asarray()
        dna6 = transform.downscale_local_mean(dna6, (2, 2))\
                .astype(dna6.dtype)
        dna6 = img_as_ubyte(dna6)

#    with tifffile.TiffFile('../data/he_img.tif') as tif:
#        he = None
#        for i in range(3):
#            he_i = tif.series[0].pages[0].asarray()[i, ...]
#            he_i = transform.downscale_local_mean(he_i, (4, 4))\
#                    .astype('uint8')
#            if he is None:
#                he = np.zeros(he_i.shape+(3,), dtype=he_i.dtype)
#            he[..., i] = he_i
#        he = color.rgb2gray(he)
#        he = img_as_ubyte(he)
#        he = 255-he

    with napari.gui_qt():
        viewer = napari.viewer.Viewer(show=False)
        viewer.add_image(dna6, name='dna6', colormap='green',
                blending='additive')
#        viewer.add_image(he, name='he', colormap='red',
#                blending='additive')
        viewer.show()
