import numpy as np
import fire

from skimage import io, util

def se_postprocessing(in_filepath: str, out_filepath: str, dtype: str):
    '''
    Post-processing for SimpleElastix output: dtype casting and range clipping.
    SimpleElastix output has roughly same value range (may exceed range of
    input data type due to interpolation) but cased to float32.

    Args:
        in_filepath, out_filepath: str
            Paths to input and output images
        dtype: str
            Image data type conversion. Accepted formats are bool, uint8, int16,
            uint16, float32, float64.
    '''
    # check dtype argument
    if dtype == 'bool':
        cast_fn = util.img_as_bool
    elif dtype == 'uint8':
        cast_fn = util.img_as_ubyte
    elif dtype == 'int16':
        cast_fn = util.img_as_int
    elif dtype == 'uint16':
        cast_fn = util.img_as_uint
    elif dtype == 'float32':
        cast_fn = util.img_as_float32
    elif dtype == 'float64':
        cast_fn = util.img_as_float64
    else:
        raise NotImplementedError('dtype {} not recognized. Currently accepted'
                'formats are bool, uint8, int16, uint16, float32, float64.'
                .format(dtype))

    # load image
    img = io.imread(in_filepath)

    # clip
    if 'float' in dtype:
        info = np.finfo(dtype)
        a_max, a_min = info.max, info.min
    elif 'int' in dtype:
        info = np.iinfo(dtype)
        a_max, a_min = info.max, info.min
    else:
        a_max, a_min = True, False

    img = np.clip(img, a_min=a_min, a_max=a_max).astype(dtype)

    # save to disk
    io.imsave(out_filepath, img)


if __name__ == '__main__':
    fire.Fire(se_postprocessing)
