import numpy as np
import pandas as pd
import tifffile

from skimage import measure

cellmask = tifffile.imread('../data/aligned_cellmask.tif')
coord = pd.DataFrame(measure.regionprops_table(label_image=cellmask,
    properties=['label', 'centroid']))
feat = pd.read_csv('../data/aligned_feature.csv')
df = coord.merge(feat, on='label', how='inner')

df['is_Bcell'] = df['CD20_bin'] > 0.2
df['xgrid'] = df['centroid-0'].apply(lambda x: np.digitize(x,
    range(300, cellmask.shape[0], 300)))
df['ygrid'] = df['centroid-1'].apply(lambda x: np.digitize(x,
    range(300, cellmask.shape[1], 300)))
df.to_csv('../data/partition.csv', index=False)
