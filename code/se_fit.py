import SimpleITK as sitk
import fire


def se_fit(fixed_filepath: str, moving_filepath: str, out_filepath: str=None,
        nres: int=4, niter: int=256):
    '''
    Register one image to another using intensity-based affine transformation
    with SimpleElastix library (C++ library with Python interface).

    Args:
        fixed_filepath, moving_filepath, out_filepath: str
            Paths of fixed, moving, and registered moving images.
        nres: int [optional]
            Number of resolutions. SimpleElastix performs multi-resolution
            algorithms; more resolution allows fewer iterations but more
            computer memory. Default is 4 layers.
        niter: int [optional]
            Maximum number of iterations. Default is 256.
    '''
    # load data
    fixed = sitk.ReadImage(fixed_filepath)
    moving = sitk.ReadImage(moving_filepath)

    # configure image filter
    img_filter = sitk.ElastixImageFilter()
    img_filter.SetFixedImage(fixed)
    img_filter.SetMovingImage(moving)

    # configure transformation
    pm = sitk.GetDefaultParameterMap('affine')
    pm['NumberOfResolutions'] = [str(nres)]
    pm['MaximumNumberOfIterations'] = [str(niter)]
    vec = sitk.VectorOfParameterMap()
    vec.append(pm)
    img_filter.SetParameterMap(vec)

    # execute registration
    img_filter.Execute()
    out = img_filter.GetResultImage()

    # save output to disk
    if out_filepath is not None:
        sitk.WriteImage(out, out_filepath)


if __name__ == '__main__':
    fire.Fire(se_fit)
