#!/usr/bin/env python3

import click
import itk
import numpy as np

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-i','--input', required=True)
@click.option('-o','--output', required=True)
@click.option('--factor','-f','factor', default = 1.1)
def scatter_correction_dew(input,output, factor):
    projections=itk.imread(input)
    array_projections=itk.array_from_image(projections).astype(float)

    nb_projections=array_projections.shape[0]
    nb_projections_per_window = nb_projections // 2

    array_projections_scatter_corrected = array_projections[:nb_projections_per_window,:,:] \
                                    - factor * array_projections[nb_projections_per_window:,:,:]

    array_projections_scatter_corrected[array_projections_scatter_corrected<0]=0

    projections_scatter_corrected=itk.image_from_array(array_projections_scatter_corrected)
    projections_scatter_corrected.CopyInformation(projections)

    itk.imwrite(projections_scatter_corrected,output)
    print('SC done!')



if __name__ == '__main__':
    scatter_correction_dew()
