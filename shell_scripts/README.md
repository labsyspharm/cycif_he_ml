# shell scripts

## Files
* `config.sh`: configuration file template
* `step_1a.sh`: TIFF --> HDF5, 1 time
* `step_1b.sh`: HDF5 --> TIFF ready for SimpleElastix, 1+N times if cropping is needed
* `step_2.sh`: TIFF + TIFF --> TIFF (registration preview) + transform params, 1+N times if need to adjust iterations and/or resolutions
* `step_3.sh`: transform params --> OME.TIFF for upload to HMS OMERO server

## Note
* Make one `config.sh` per sample processed and copy to project folder
* Leave this repo folder `cycif_he_ml` at one central location (ex. home directory) and call the scripts like `bash ~/cycif_he_ml/shell_scripts/step_1a.sh ./config.sh`
* Memory requirement: for uint16 images of shape (30k, 20k), step 1a, 1b, 3 require 64 GB RAM and step 2 require 100-200 GB RAM (depending on resolutions)
* Runtime requirement: 1 hr for step 1a, 1b, 3, and 3 hr for step 2 (8 resolutions and 10k iterations)
