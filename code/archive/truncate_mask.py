import tifffile

mask = tifffile.imread('../data/cellRingMask_downscaled.tif')
dna = tifffile.imread('../data/aligned_DNA6.tif')
mask = mask[:dna.shape[0], :dna.shape[1]]
tifffile.imsave('../data/aligned_cellmask.tif', mask)
