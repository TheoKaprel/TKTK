#!/export/home/tkaprelian/Software/miniconda3/bin/python

import itk
import click

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('--i1','image1', help = 'input image 1')
@click.option('--i2', 'image2', help = 'input image 2')
@click.option('-o', '--output', help = 'output filename')

def sum_itk_images(image1, image2, output):
    
    img1 = itk.imread(image1)
    img2 = itk.imread(image2)
    
    array1 = itk.array_view_from_image(img1)
    array2 = itk.array_view_from_image(img2)
    
    array_sum = array1+array2
    image_sum = itk.image_from_array(array_sum)
    image_sum.CopyInformation(img1)

    itk.imwrite(image_sum, output)
    print(f'The sum of {image1} and {image2} saved in {output} !')



if __name__=='__main__':
    sum_itk_images()