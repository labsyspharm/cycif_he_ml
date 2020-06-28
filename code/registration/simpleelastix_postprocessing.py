import sys
import numpy as np
from skimage import io

if __name__ == '__main__':
    # path
    in_filepath = sys.argv[1]
    out_filepath = sys.argv[2]
    dtype = sys.argv[3]

    # clip and save to disk
    img = io.imread(in_filepath)
    try:
        a_max = np.iinfo(dtype).max
    except:
        a_max = np.finfo(dtype).max
    img = np.clip(img, a_min=0, a_max=a_max)
    img = img.astype(dtype)
    io.imsave(out_filepath, img)
