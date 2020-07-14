import SimpleITK as sitk
import fire


def se_fit(fixed_filepath: str, moving_filepath: str):
    """
    Register one image to another using intensity-based affine transformation
    with SimpleElastix library (C++ library with Python interface).

    Args:
        fixed_filepath, moving_filepath: str
            Paths of fixed and moving images.
    """
    # configure image filter
    img_filter = sitk.ElastixImageFilter()
    img_filter.SetFixedImage(sitk.ReadImage(fixed_filepath))
    img_filter.SetMovingImage(sitk.ReadImage(moving_filepath))

    # configure transformation
    params_d = {
        # main components
        "Registration": ["MultiResolutionRegistration"],
        "Interpolator": ["BSplineInterpolator"],
        "ResampleInterpolator": ["FinalBSplineInterpolator"],
        "Resampler": ["DefaultResampler"],
        "FixedImagePyramid": ["FixedRecursiveImagePyramid"],
        "MovingImagePyramid": ["MovingRecursiveImagePyramid"],
        "Optimizer": ["AdaptiveStochasticGradientDescent"],
        "Metric": ["AdvancedMattesMutualInformation"],
        # transformation
        "FinalGridSpacingInVoxels": ["20"],
        # multi-resolution
        "NumberOfResolutions": ["4"],
        # optimizer
        "MaximumNumberOfIterations": ["3000"],
        # sampling to compute mutual information
        "NumberOfSpatialSamples": ["4096"],
        "NewSamplesEveryIteration": ["true"],
        "ImageSampler": ["Random"],
        # interpolation
        "FinalBSplineInterpolationOrder": ["3"],
        "DefaultPixelValue": ["0"],
        # output
        "WriteResultImage": ["true"],
        "ResultImageFormat": ["tif"],
    }
    discard_list = ['FinalGridSpacingInPhysicalUnits']
    mode_list = ["translation", "affine", "bspline"]

    vec = sitk.VectorOfParameterMap()
    for mode in mode_list:
        pm = sitk.GetDefaultParameterMap(mode)
        for k in params_d:
            pm[k] = params_d[k]
        for k in discard_list:
            if k in pm:
                del pm[k]
        vec.append(pm)
    img_filter.SetParameterMap(vec)

    # execute registration
    img_filter.Execute()
    sitk.WriteImage(img_filter.GetResultImage(), "out.tif")


if __name__ == "__main__":
    fire.Fire(se_fit)
