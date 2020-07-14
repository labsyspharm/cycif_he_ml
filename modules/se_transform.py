import SimpleITK as sitk
import fire


def se_transform(param_filepath: str, moving_filepath: str, out_filepath: str):
    '''
    Transform known mapping to other images.

    Args:
        param_filepath, moving_filepath, out_filepath: str
            Paths to parameter, moving image, and output image.
    '''
    # load data
    img_in = sitk.ReadImage(moving_filepath)
    paramMap = sitk.ReadParameterFile(param_filepath)

    # perfrom transformation
    img_out = sitk.Transformix(img_in, paramMap)

    # save to disk
    sitk.WriteImage(img_out, out_filepath)


if __name__ == '__main__':
    fire.Fire(se_transform)
