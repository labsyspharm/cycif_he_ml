import numpy as np
import tifffile
import dask
import dask.array as da
import napari
import napari.viewer as nv

from skimage import io, transform

def load_tif(path, shape=None):
    with tifffile.TiffFile(path) as tif:
        img = tif.series[0].pages[0].asarray()
    if shape is not None:
        img = transform.resize(img, shape)
    return img

def main():
    cycif_filepath = '../data_cycif_he_ml/tnp_data/cycif_dna1.tif'
    cycif = io.imread(cycif_filepath)

    he_filepath = '../data_cycif_he_ml/tnp_data/he_img.tif'
    delayed_array = dask.delayed(
            lambda p: load_tif(p, cycif.shape),
            )(he_filepath)
    img = da.from_delayed(
            delayed_array,
            shape=(3, np.nan, np.nan),
            dtype=np.uint16,
            )
    img = img.compute()

    with napari.gui_qt():
        viewer = nv.Viewer(show=False)
        for i, c in enumerate(['red', 'green', 'blue']):
            viewer.add_image(img[i, ...], name=c, colormap=c, blending='additive')
        viewer.add_image(cycif, name='dna1', colormap='gray', blending='additive')
        viewer.show()

if __name__ == '__main__':
    main()
