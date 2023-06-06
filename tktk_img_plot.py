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
@click.option('-x', is_flag=True, default = False)
@click.option('-y', is_flag=True, default = False)
@click.option('-z', is_flag=True, default = False)
@click.option('--norm', is_flag=True, default = False)
@click.option('--legend')
def print_hi(image, slice, profile, x, y, z, norm, legend):
    # fig_img,ax_img_arr = plt.subplots(1,len(image))
    fig_img,ax_img_arr = plt.subplots(2,2)
    ax_img = ax_img_arr.ravel()


    stack_slices = []
    for img in (image):
        img_array = itk.array_from_image(itk.imread(img))
        if norm:
            img_array = img_array / np.sum(img_array)

        if z:
            stack_slices.append(img_array[slice,:,:])
        elif x:
            stack_slices.append(img_array[:, slice, :])
        elif y:
            stack_slices.append(img_array[:, :, slice])

    # vmin_ = min([np.min(sl) for sl in stack_slices])
    vmin_ = 0
    vmax_ = max([np.max(sl) for sl in stack_slices])

    if legend is None:
        legend = image
    else:
        legend = legend.split(',')

    for k in range(len(image)):
        imsh = ax_img[k].imshow(stack_slices[k], vmin = vmin_, vmax = vmax_)
        ax_img[k].set_title(legend[k])
        ax_img[k].axis('off')

    cb = fig_img.colorbar(imsh, ax=ax_img)
    cb.remove()

    # plt.suptitle(f'Slice {slice}')

    if profile:
        fig_prof,ax_prof = plt.subplots()
        for k in range(len(image)):
            ax_prof.plot(stack_slices[k][profile,:], '-',label = image[k])

        plt.legend()


    plt.show()





if __name__ == '__main__':
    print_hi()
