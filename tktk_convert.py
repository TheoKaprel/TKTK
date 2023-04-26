#!/usr/bin/env python3

import argparse
import numpy as np
import itk

def get_extension(filename):
    return filename.split('.')[-1]

def main():
    print(args)

    spacing_ = [float(s) for s in args.spacing.split(',')]
    if len(spacing_)==1:
        spacing_==[spacing_[0], spacing_[0], spacing_[0]]
    elif len(spacing_)!=3:
        print("ERROR: spacing error. Ex: --spacing 13.12,13.12,17.89")
        exit(0)


    input_ext = get_extension(args.input)
    output_ext = get_extension(args.output)

    if input_ext=="npy":
        assert(args.spacing is not None)
        input_img = np.load(args.input)
        input_shape = input_img.shape
        input_shape = input_shape[::-1]
        output_img = itk.image_from_array(input_img.astype(np.float32))

        output_spacing = np.array(spacing_)
        output_origin = [(-input_shape[k] * output_spacing[k] + output_spacing[k]) / 2 for k in range(3)]

        output_img.SetSpacing(output_spacing)
        output_img.SetOrigin(output_origin)
        itk.imwrite(output_img, args.output)
        print('done')




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("output")
    parser.add_argument("--spacing", type = str)
    args = parser.parse_args()

    main()
