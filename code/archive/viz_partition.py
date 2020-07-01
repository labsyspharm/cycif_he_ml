import numpy as np
import pandas as pd
import tifffile

he = tifffile.imread('../data/aligned_he.tif')
grid_shape = (
        int(np.ceil(he.shape[0]/300)),
        int(np.ceil(he.shape[1]/300)),
        )

df = pd.read_csv('../data/partition.csv')
tile_coord = df.groupby(['xgrid', 'ygrid'])['is_Bcell'].agg(['mean', 'count'])\
        .reset_index(drop=False)\
        .rename(columns={'mean': 'frac_Bcell', 'count': 'num_cell'})
tile_coord['tile_id'] = tile_coord[['xgrid', 'ygrid']].apply(
        lambda row: np.ravel_multi_index(row, grid_shape), axis=1)

for index in tile_coord.index:
    xg, yg = tile_coord.loc[index, ['xgrid', 'ygrid']].values.astype(int)
    xl, xu = xg*300, min((xg+1)*300, he.shape[0])
    yl, yu = yg*300, min((yg+1)*300, he.shape[1])
    tile = he[xl:xu, yl:yu]
    tile_id = tile_coord.loc[index, 'tile_id']
    tifffile.imsave('../data/he_tiles/he_tile_{}.tif'.format(tile_id), tile)

tile_coord.to_csv('../data/he_tiles/he_tile_table.csv', index=False)
