#!/usr/bin/env python3

import click
import itk
import numpy as np
import matplotlib.pyplot as plt

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-i', '--image', multiple = True, help = 'Input image')
@click.option('-s','--slice', type = int)
@click.option('-p','--profile', type = int)
def print_hi(image, slice, profile):
    fig_img,ax_img = plt.subplots(1,len(image))


    stack_slices = []
    for img in (image):
        img_array = itk.array_from_image(itk.imread(img))

        stack_slices.append(img_array[slice,:,:])

    vmin_ = min([np.min(sl) for sl in stack_slices])
    vmax_ = max([np.max(sl) for sl in stack_slices])


    for k in range(len(image)):
        imsh = ax_img[k].imshow(stack_slices[k], vmin = vmin_, vmax = vmax_)
        ax_img[k].set_title(image[k])

    fig_img.colorbar(imsh, ax=ax_img)

    plt.suptitle(f'Slice {slice}')

    if profile:
        fig_prof,ax_prof = plt.subplots()
        for k in range(len(image)):
            ax_prof.plot(stack_slices[k][profile,:], '-',label = image[k])

        plt.legend()


    plt.show()





if __name__ == '__main__':
    print_hi()
