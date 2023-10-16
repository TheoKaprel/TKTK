#!/usr/bin/env python3

import click
import itk
import numpy as np
import matplotlib.pyplot as plt

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-i', '--image', multiple = True, help = 'Input image')
@click.option('-s','--slice', type = int, multiple=True)
@click.option('-p','--profile', type = int)
@click.option('-x', is_flag=True, default = False)
@click.option('-y', is_flag=True, default = False)
@click.option('-z', is_flag=True, default = False)
@click.option('--norm', is_flag=True, default = False)
@click.option('--legend')
def print_hi(image, slice, profile, x, y, z, norm, legend):
    n_img = len(image)*len(slice)
    if n_img==1:
        n_lines,n_col = 1,1
    elif n_img==2:
        n_lines,n_col = 1,2
    else:
        n_lines = 2
        n_col = n_img//2


    fig_img,ax_img_arr = plt.subplots(n_lines,n_col)
    ax_img = ax_img_arr.ravel() if n_img>1 else [ax_img_arr]


    stack_slices = []
    for slice_ in slice:
        for img in (image):
            print(img)
            img_array = read_to_array(img)
            if norm:
                img_array = img_array / np.sum(img_array)

            if z:
                stack_slices.append(img_array[slice_,:,:].astype(np.float))
            elif x:
                stack_slices.append(img_array[:, slice_, :].astype(np.float))
            elif y:
                stack_slices.append(img_array[:, :, slice_].astype(np.float))

    # vmin_ = min([np.min(sl) for sl in stack_slices])
    vmin_ = 0
    vmax_ = max([np.max(sl) for sl in stack_slices])

    if legend is None:
        legend = image
    else:
        legend = legend.split(',')
    print(legend)
    for k in range(len(stack_slices)):
        imsh = ax_img[k].imshow(stack_slices[k], vmin = vmin_, vmax = vmax_)
        ax_img[k].set_title(legend[k])
    for k in range(len(ax_img)):
        ax_img[k].axis('off')

    # cb = fig_img.colorbar(imsh, ax=ax_img)
    # cb.remove()
    fig_img.subplots_adjust(right=0.8)
    cbar_ax = fig_img.add_axes([0.85, 0.15, 0.05, 0.7])
    fig_img.colorbar(imsh, cax=cbar_ax)

    # plt.suptitle(f'Slice {slice}')

    if profile:
        fig_prof,ax_prof = plt.subplots()
        for k in range(len(image)):
            ax_prof.plot(stack_slices[k][profile,:], '-',label = image[k])

        plt.legend()


    plt.show()



def read_to_array(filename):
    ext = filename.split('.')[-1]
    if (ext=='mhd' or ext=='mha'):
        return itk.array_from_image(itk.imread(filename))
    elif (ext=='npy'):
        return np.load(filename)

if __name__ == '__main__':
    print_hi()
