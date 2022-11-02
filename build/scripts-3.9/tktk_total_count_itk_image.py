#!/export/home/tkaprelian/Software/miniconda3/bin/python

import itk
import click
import numpy as np

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-i','image', help = 'input image')
@click.option('--slicej', type = int)
def calc_total_counts(image, slicej):
    
    img = itk.imread(image)
    
    array = itk.array_view_from_image(img)

    print(array.shape)

    if slicej == None:
        total_counts = np.sum(array)
        print(f'Total counts in image {image}  :  {total_counts}!')
    else:
        total_counts = np.sum(array[slicej,:,:])
        print(f'Total counts in slice {slicej} of image {image}  :  {total_counts}!')



if __name__=='__main__':
    calc_total_counts()
