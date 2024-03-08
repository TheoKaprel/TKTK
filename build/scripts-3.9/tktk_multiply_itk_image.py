#!python


import itk
import click

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-i', '--image', help = 'Input image', required = True)
@click.option('-f', '--factor', help = 'Factor by each you want to multiply he input', required = True)
@click.option('-o', '--output', 'output_fn', required = True)
def multiply_itk_image(image, factor, output_fn):
    img = itk.imread(image)
    img_array = itk.array_from_image(img)

    img_array = img_array * float(factor)

    img_multiplied = itk.image_from_array(img_array)
    img_multiplied.CopyInformation(img)

    itk.imwrite(img_multiplied, output_fn)
    print(f'Done! Output at {output_fn}')




if __name__=='__main__':
    multiply_itk_image()
