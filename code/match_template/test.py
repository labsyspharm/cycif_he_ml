import numpy as np
import skimage.data
from skimage.color import rgb2gray
from skimage.morphology import disk, square
import dask.array as da
from skimage_match_template import match_template as skmt
from dask_match_template import match_template as damt

img = skimage.data.astronaut()
img = rgb2gray(img)
img = da.from_array(img)
p = dict(image=img, template=square(3), mode='constant', pad_input=True)

skres = skmt(**p)
dares = damt(**p).compute()

print(np.array_equal(skres, dares))
