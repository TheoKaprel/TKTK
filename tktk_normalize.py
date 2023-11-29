#!/usr/bin/env python3

import argparse
import itk
import numpy as np

def get_ext(fn):
    return fn.split('.')[-1]


def main():
    print(args)

    for img in args.inputs:
        ext=get_ext(img)
        if ext in ['mhd','mha']:
            img_itk = itk.imread(img)
            img_array = itk.array_from_image(img_itk)


        if args.norm=="sum":
            img_array = img_array/img_array.sum()
        elif args.norm=="act":
            img_array = img_array/img_array.sum() * args.act

        new_img_itk=itk.image_from_array(img_array)
        new_img_itk.CopyInformation(img_itk)
        normed_fn = img.replace(f'.{ext}', f'_normed.{ext}')
        itk.imwrite(new_img_itk,normed_fn)
        print(normed_fn)



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("inputs", nargs='+')
    parser.add_argument("--norm",choices=['sum', 'act'])
    parser.add_argument("--act",type=float)
    args = parser.parse_args()

    main()
