import itk
import click

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-i','input_file_name', help = 'input filename')
@click.option('-s', '--output_spacing')
@click.option('--output_size')
@click.option('-o', '--output_file_name')
@click.option('--interpolator', type=click.Choice(['linear', 'nearest_neighbor']))
def resample(input_file_name, output_spacing,output_size, output_file_name, interpolator):
    input_image = itk.imread(input_file_name)
    input_size = itk.size(input_image)
    input_spacing = itk.spacing(input_image)
    input_origin = itk.origin(input_image)

    output_spacing = [float(output_spacing), float(output_spacing), float(output_spacing)]
    if output_size==None:
        output_size = [int(input_spacing[k]*input_size[k]/output_spacing[k]) for k in range(3)]
    else:
        output_size = int(output_size)
    output_origin = input_origin

    if interpolator=='linear':
        m_interpolator = itk.LinearInterpolateImageFunction.New(input_image)
    elif interpolator=='nearest_neighbor':
        m_interpolator = itk.NearestNeighborInterpolateImageFunction.New(input_image)



    resampled = itk.resample_image_filter(
        input_image,
        interpolator=m_interpolator,
        size=output_size,
        output_spacing=output_spacing,
        output_origin=output_origin,
        default_pixel_value = 0
    )

    itk.imwrite(resampled, output_file_name)

#
# EXAMPLE
# resample('./data/acf_ct_air.mhd', output_spacing=[7,7,7], output_file_name='./data/acf_ct_air_resampled.mhd')



if __name__=='__main__':
    resample()