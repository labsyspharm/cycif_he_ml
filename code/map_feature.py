import numpy as np
import pandas as pd
import tifffile

mask = tifffile.imread('../data/aligned_cellmask.tif')
df = pd.read_csv('../data/aligned_feature.csv')
df.set_index('label', inplace=True)
map_d = df['CD20_bin'].to_dict()

map_d[0] = 0.0
map_feat = np.vectorize(lambda x: map_d[x])(mask)
tifffile.imsave('../data/CD20_bin_map.tif', map_feat)

df['cluster'] = df['CD20_bin'].apply(lambda x: np.digitize(x, [0.2]))+1
map_c = df['cluster'].to_dict()
map_c[0] = 0
map_cluster = np.vectorize(lambda x: map_c[x])(mask)
tifffile.imsave('../data/CD20_cluster_map.tif', map_cluster)
