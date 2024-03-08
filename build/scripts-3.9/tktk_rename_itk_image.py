#!python

import click
import itk
import os

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-i','--input')
@click.option('-o','--output')
@click.option('--keep', is_flag=True, default=False, help="If you want to keep the input")
def print_hi(input, output, keep):

    input_img=itk.imread(input)
    itk.imwrite(input_img,output)

    if keep==False:
        os.remove(input)
        os.remove(input.replace('mhd', 'raw'))



if __name__ == '__main__':
    print_hi()
