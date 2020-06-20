import pandas as pd
import tifffile

from skimage import measure

if __name__ == '__main__':
    mask = tifffile.imread('../data/cellRingMask_downscaled.tif')
    dna6 = tifffile.imread('../data/aligned_DNA6.tif')
    cd20 = tifffile.imread('../data/aligned_CD20.tif')

    mask = mask[:dna6.shape[0], :dna6.shape[1]]

    p = measure.regionprops_table(label_image=mask, intensity_image=dna6,
            properties=['label', 'mean_intensity'])
    df1 = pd.DataFrame(p).rename(columns={'mean_intensity': 'DNA6'})

    p = measure.regionprops_table(label_image=mask, intensity_image=cd20,
            properties=['label', 'mean_intensity'])
    df2 = pd.DataFrame(p).rename(columns={'mean_intensity': 'CD20'})

    df = df1.merge(df2, on='label', how='inner')
    df.to_csv('../data/aligned_feature.csv', index=False)
