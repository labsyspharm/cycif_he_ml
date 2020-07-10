import tifffile
import numpy as np
import fire

def prep(filelist_filepath: str, out_filepath: str):
    '''
    Prepare for Bioformats bfconvert
    '''
    with open(filelist_filepath, 'r') as f:
        img_list = [tifffile.imread(fp.strip()) for fp in f]
    img = np.stack(img_list, axis=0)[..., np.newaxis]
    tifffile.imsave(out_filepath, img)

if __name__ == '__main__':
    fire.Fire(prep)
