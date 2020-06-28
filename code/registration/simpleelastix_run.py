'''
Modified from https://simpleelastix.readthedocs.io/NonRigidRegistration.html
'''
import sys
import SimpleITK as sitk

if __name__ == '__main__':
    # path
    fixed_filepath = sys.argv[1]
    moving_filepath = sys.argv[2]
    out_filepath = sys.argv[3]

    # load data
    elastixImageFilter = sitk.ElastixImageFilter()
    elastixImageFilter.SetFixedImage(sitk.ReadImage(fixed_filepath))
    elastixImageFilter.SetMovingImage(sitk.ReadImage(moving_filepath))

    # configure transformation
    pm = sitk.GetDefaultParameterMap('affine')
    pm['NumberOfResolutions'] = ['16']
    pm['MaximumNumberOfIterations'] = ['3072']
    parameterMapVector = sitk.VectorOfParameterMap()
    parameterMapVector.append(pm)
    elastixImageFilter.SetParameterMap(parameterMapVector)

    # run registration
    elastixImageFilter.Execute()

    # save output to disk
    sitk.WriteImage(elastixImageFilter.GetResultImage(), out_filepath)
