#!python

import click
import numpy as np
import itk

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-i','--image', help = 'input image')
@click.option('-m','--min', type = float, help = 'min threshold')
@click.option('-M','--max', type = float, help = 'max threshold')
@click.option('--vm', 'value_min', type = float)
@click.option('--vM', 'value_max', type = float)
@click.option('-o', 'output_filename')
def thresh_img(image, min, max, value_min, value_max, output_filename):
    if value_min==None:
        value_min = min
    if value_max==None:
        value_max = max


    input_img = itk.imread(image)
    input_array = itk.array_from_image(input_img)

    if min:
        input_array[input_array<min] = value_min

    if max:
        input_array[input_array>max] = value_max

    output_image = itk.image_from_array(input_array)
    output_image.CopyInformation(input_img)
    itk.imwrite(output_image, output_filename)



if __name__ == '__main__':
    thresh_img()
