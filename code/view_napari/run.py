import os

import numpy as np
import h5py
import dask.array as da
import napari
import napari.viewer as nv

if __name__ == '__main__':
    # paths
    hdf5_folderpath = '/home/hungyiwu/Desktop/data_cycif_he_ml/tnp_data/'\
            'derived_data/hdf5'
    he_filename = 'TNP_96.hdf5'
    cycif_filename = 'WD-76845-097.hdf5'

    # load data
    he_file = h5py.File(os.path.join(hdf5_folderpath, he_filename), 'r')
    cycif_file = h5py.File(os.path.join(hdf5_folderpath, cycif_filename), 'r')
    he_arr = da.from_array(he_file['b'], chunks=(5000, 5000))
    cycif_arr = da.from_array(cycif_file['DNA1'], chunks=(5000, 5000))

    # add to napari
    with napari.gui_qt():
        v = nv.Viewer(show=False)
        v.add_image(np.iinfo(he_arr.dtype).max - he_arr, multiscale=False,
                contrast_limits=[0, np.iinfo(he_arr.dtype).max])
        v.add_image(cycif_arr, multiscale=False,
                contrast_limits=[0, np.iinfo(cycif_arr.dtype).max])
        v.show()
