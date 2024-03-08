#!python

import click
import itk
import numpy as np

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('--sinogram')
@click.option('--pw')
@click.option('--sw')
@click.option('-o','--output', required=True)
@click.option('--factor','-f','factor', default = 1.1)
@click.option('--img', is_flag=True, default=False)
def scatter_correction_dew(sinogram,pw,sw,output, factor,img):

    if (sinogram is not None) and ((pw is not None) or (sw is not None)):
        print('ERROR: choose between --sinogram (containing both PW and SW) or give both --pw and --sw separetely')
        exit(0)
    if ((pw is not None) and (sw is None)) or ((pw is None) and (sw is not None)):
        print('ERROR: --pw and --sw are needed')
        exit(0)
    if ((sinogram is None) and (pw is None) and (sw is None)):
        print('ERROR: no input. Choose between --sinogram (containing both PW and SW) or give both --pw and --sw separetely')
        exit(0)


    if ((sinogram is not None) and (pw is None) and (sw is None)):
        projections=itk.imread(sinogram)
        array_projections=itk.array_from_image(projections).astype(float)

        nb_projections=array_projections.shape[0]
        nb_projections_per_window = nb_projections // 2

        array_PW = array_projections[:nb_projections_per_window,:,:]
        array_SW = array_projections[nb_projections_per_window:,:,:]

        input_size = np.array(itk.size(projections))
        input_spacing = np.array(itk.spacing(projections))

    elif ((sinogram is None) and (pw is not None) and (sw is not None)):
        projections_PW = itk.imread(pw)
        projections_SW = itk.imread(sw)

        array_PW= itk.array_from_image(projections_PW)
        array_SW= itk.array_from_image(projections_SW)

        input_size = np.array(itk.size(projections_PW))
        input_spacing = np.array(itk.spacing(projections_PW))


    output_origin = [(-input_size[k] * input_spacing[k] + input_spacing[k]) / 2 for k in range(3)]

    if img==False:
        output_origin[2] = 0

    output_direction = np.eye(3)

    array_projections_scatter_corrected =  array_PW - factor * array_SW
    array_projections_scatter_corrected[array_projections_scatter_corrected<0]=0

    projections_scatter_corrected=itk.image_from_array(array_projections_scatter_corrected)

    projections_scatter_corrected.SetSpacing(input_spacing)
    projections_scatter_corrected.SetOrigin(output_origin)
    projections_scatter_corrected.SetDirection(output_direction)

    itk.imwrite(projections_scatter_corrected,output)
    print('SC done!')



if __name__ == '__main__':
    scatter_correction_dew()
