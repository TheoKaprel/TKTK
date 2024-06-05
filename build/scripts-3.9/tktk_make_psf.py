#!python

import argparse
import itk
import numpy as np
import torch

def main():
    print(args)
    k = args.kernel_size
    xk = torch.arange(k)
    x, y, z = torch.meshgrid(xk, xk, xk, indexing="ij")

    m = (k - 1) / 2

    fx,fy,fz = args.x, args.y,args.z
    c =  2 * np.sqrt(2*np.log(2))
    sx_,sy_,sz_ = fx/c, fy/c, fz/c

    spacing = args.spacing
    sx, sy, sz = sx_/spacing, sy_/spacing, sz_/spacing


    N = np.sqrt(2 * np.pi) ** 3 * sx * sy * sz

    f = 1. / N * torch.exp(-((x - m) ** 2 / sx ** 2 + (y - m) ** 2 / sy ** 2 + (z - m) ** 2 / sz ** 2) / 2)
    f = f/f.sum()

    if args.output.split(".")[-1]=="mhd":
        img = itk.image_from_array(f.numpy())
        itk.imwrite(img, args.output)
    else:
        np.save(args.output, f.numpy())


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--kernel_size", '-k', type =int)
    parser.add_argument("-x",type =float)
    parser.add_argument("-y",type =float)
    parser.add_argument("-z",type =float)
    parser.add_argument("--spacing",type =float)
    parser.add_argument("--output","-o")
    args = parser.parse_args()

    main()
