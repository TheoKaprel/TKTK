#!/usr/bin/env python3

import argparse
import itk
import numpy as np
import matplotlib.pyplot as plt


def print_hi(image, slice, profile, axis, norm, legend):
    n_img = len(image)*len(slice)
    if n_img==1:
        n_lines,n_col = 1,1
    elif n_img==2:
        n_lines,n_col = 1,2
    else:
        n_lines = 2
        n_col = n_img//2 if n_img%2==0 else n_img//2+1


    fig_img,ax_img_arr = plt.subplots(n_lines,n_col)
    ax_img = ax_img_arr.ravel() if n_img>1 else [ax_img_arr]


    stack_slices = []
    # legend=[]
    for slice_ in slice:
        for img in (image):
            print(img)
            img_array = read_to_array(img)
            if norm:
                img_array = img_array / np.sum(img_array)

            if axis=="z":
                stack_slices.append(img_array[slice_,:,:].astype(np.float32))
            elif axis=="y":
                stack_slices.append(img_array[:, slice_, :].astype(np.float32))
            elif axis=="x":
                stack_slices.append(img_array[:, :, slice_].astype(np.float32))
            # legend.append(img)
    # vmin_ = min([np.min(sl) for sl in stack_slices])
    vmin_ = 0
    vmax_ = max([np.max(sl) for sl in stack_slices])

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
        color = ["dimgrey","black", "blue", "blueviolet", "#f9bc08", "orangered", "#ff9408"]
        fig_prof,ax_prof = plt.subplots()
        for k in range(len(stack_slices)):
            ax_prof.plot(stack_slices[k][profile,:], '-',label = legend[k], color = color[k], linewidth = 1.5)

        ax_prof.set_xlabel("Pixels", fontsize = 20)
        ax_prof.set_ylabel("Reconstructed Counts", fontsize = 20)
        plt.legend(fontsize=20)


    plt.show()



def read_to_array(filename):
    ext = filename.split('.')[-1]
    if (ext=='mhd' or ext=='mha'):
        return itk.array_from_image(itk.imread(filename))
    elif (ext=='npy'):
        return np.load(filename)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i","--images",type = str, nargs = "*")
    parser.add_argument("-s","--slice",type = int, nargs = "*")
    parser.add_argument("-p","--profile",type = int)
    parser.add_argument("--axis", choices = ["x", "y", "z"])
    parser.add_argument("--norm", action="store_true")
    parser.add_argument("--legend",type = str, nargs = "*")
    args = parser.parse_args()
    print_hi(image = args.images, slice=args.slice, profile=args.profile,axis= args.axis, norm=args.norm, legend=args.legend)

# CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
# @click.command(context_settings=CONTEXT_SETTINGS)
# @click.option('-i', '--image', multiple = True, help = 'Input image')
# @click.option('-s','--slice', type = int, multiple=True)
# @click.option('-p','--profile', type = int)
# @click.option('-x', is_flag=True, default = False)
# @click.option('-y', is_flag=True, default = False)
# @click.option('-z', is_flag=True, default = False)
# @click.option('--norm', is_flag=True, default = False)
# @click.option('--legend')