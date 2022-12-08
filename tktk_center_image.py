#!/usr/bin/env python3

import click
import numpy as np
import itk

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-i','--input')
@click.option('-o','--output')
def center(input, output):
    input_image = itk.imread(input)
    input_size = np.array(itk.size(input_image))
    input_spacing = np.array(itk.spacing(input_image))

    output_origin = [(-input_size[k]*input_spacing[k] + input_spacing[k])/2 for k in range(3)]

    input_image.SetOrigin(output_origin)
    itk.imwrite(input_image, output)


if __name__ == '__main__':
    center()
