import functools

import pandas as pd
import tifffile

from skimage import measure

if __name__ == '__main__':
    mask = tifffile.imread('../data/aligned_cellmask.tif')
    dna6 = tifffile.imread('../data/aligned_DNA6.tif')
    cd20 = tifffile.imread('../data/aligned_CD20.tif')
    cd20_bin = tifffile.imread('../data/aligned_CD20_binmask.tif')

    col = {'DNA6': dna6, 'CD20': cd20, 'CD20_bin': cd20_bin}
    df_list = []
    for k in col:
        p = measure.regionprops_table(
                label_image=mask,
                intensity_image=col[k],
                properties=['label', 'mean_intensity'],
                )
        df = pd.DataFrame(p).rename(columns={'mean_intensity': k})
        df_list.append(df)

    df = functools.reduce(lambda x,y: x.merge(y, on='label', how='inner'),
            df_list)
    df.to_csv('../data/aligned_feature.csv', index=False)
