#!/bin/bash
python tiff2hdf5.py he_tiff2hdf5.yaml
python rgb2gray.py he_rgb2gray.yaml
python tiff2hdf5.py cycif_tiff2hdf5.yaml
