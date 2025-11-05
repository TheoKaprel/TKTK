#!/usr/bin/env python3

import argparse
import itk
import numpy as np


def main():
    print(args)

    out = None
    for inpu_fn in args.inputs:
        if out is None:
            img = itk.imread(inpu_fn)
            array = itk.array_from_image(img)
            out = array
        else:
            array = itk.array_from_image(itk.imread(inpu_fn))
            max_lbl = out.max()
            array[array>0]+=max_lbl
            out[array>0] = array[array>0]

    out_img = itk.image_from_array(out)
    out_img.CopyInformation(img)
    itk.imwrite(out_img, args.output)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputs", nargs="+")
    parser.add_argument("--output")
    args = parser.parse_args()

    main()
