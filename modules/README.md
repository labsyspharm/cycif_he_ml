# Python code modules

## Utility modules
* `tiff2hdf5.py`: convert TIFF to HDF5 format for more memory-efficient access
* `downscale.py`: downscale HDF5 images in case of out-of-memory issues
* `rgb2gray.py`: make composite gray-scale of H&E for registration
* `make_pyramid.py` routine required before uploading to HMS OMERO server

## SimpleElastix modules
* `se_prep.py`: various pre-processing stuffed here for convenience
* `se_fit.py`: affine transform only, changing iterations and resolutions
* `se_fit_nonlinear.py` experimental bspline transform, not thoroughly tested
* `se_postprocessing.py` necessary, range clipping and dtype conversion
* `se_transform.py`: apply existing transform to more images

## External modules
* `ashlar_pyramid.py`: specifically designed for HMS OMERO server ([source](https://gist.github.com/jmuhlich/a926f55f7eb115af54c9d4754539bbc1))
