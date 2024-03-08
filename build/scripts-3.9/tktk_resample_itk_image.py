#!python

import itk
import click
import numpy as np

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-i','input_file_name', help = 'input filename', required = True)
@click.option('--output_spacing', nargs = 3)
@click.option('--output_size', nargs=3)
@click.option('--like')
@click.option('-o', '--output_file_name', required = True)
@click.option('--interpolator', type=click.Choice(['linear', 'nearest_neighbor']), default='linear', show_default = True)
def resample(input_file_name, output_spacing,output_size,like, output_file_name, interpolator):
    input_image = itk.imread(input_file_name)
    input_size = itk.size(input_image)
    input_spacing = itk.spacing(input_image)
    input_origin = itk.origin(input_image)


    if like:
        like_img = itk.imread(like)
        output_spacing3D = itk.spacing(like_img)
        output_size3D = itk.size(like_img)
        output_origin3D = itk.origin(like_img)
    else:
        output_spacing3D = np.array([float(output_spacing[k]) for k in range(3)])
        if output_size==None:
            output_size3D = [int(input_spacing[k]*input_size[k]/output_spacing3D[k]) for k in range(3)]
        else:
            output_size3D = [int(output_size[k]) for k in range(3)]
        # output_origin3D = [(-output_size3D[k] * output_spacing3D[k] + output_spacing3D[k]) / 2 for k in range(3)]
        output_origin3D = input_origin + (output_spacing3D - input_spacing)/2

    if interpolator=='linear':
        m_interpolator = itk.LinearInterpolateImageFunction.New(input_image)
    elif interpolator=='nearest_neighbor':
        m_interpolator = itk.NearestNeighborInterpolateImageFunction.New(input_image)

    resampled = itk.resample_image_filter(
        input_image,
        interpolator=m_interpolator,
        size=output_size3D,
        output_spacing=output_spacing3D,
        output_origin=output_origin3D,
        default_pixel_value = 0
    )

    itk.imwrite(resampled, output_file_name)

#
# EXAMPLE
# resample('./data/acf_ct_air.mhd', output_spacing=[7,7,7], output_file_name='./data/acf_ct_air_resampled.mhd')



if __name__=='__main__':
    resample()