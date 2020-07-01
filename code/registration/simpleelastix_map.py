import sys
import SimpleITK as sitk

if __name__ == '__main__':
    # path
    param_filepath = sys.argv[1]
    moving_filepath = sys.argv[2]
    out_filepath = sys.argv[3]

    # load, run, save
    img_in = sitk.ReadImage(moving_filepath)
    paramMap = sitk.ReadParameterFile(param_filepath)
    img_out = sitk.Transformix(img_in, paramMap)
    sitk.WriteImage(img_out, out_filepath)
