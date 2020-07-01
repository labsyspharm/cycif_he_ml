import numpy as np
import pandas as pd
import tifffile

df = pd.read_csv('../data/he_tiles/he_tile_table.csv')\
        .set_index('tile_id')
df = df.loc[df['num_cell']>10]
d = df['frac_Bcell'].to_dict()

arr_list = []
frac_list = []
for k in d:
    p = '../data/he_tiles/he_tile_{}.tif'.format(k)
    tile = tifffile.imread(p)
    if tile.shape == (300, 300):
        arr_list.append(tile)
        frac_list.append(d[k])

arr = np.stack(arr_list, axis=0)
frac = np.array(frac_list)
np.save('../data/he_tile_X.npy', arr)
np.save('../data/he_tile_y.npy', frac)

print(arr.shape, frac.shape)
