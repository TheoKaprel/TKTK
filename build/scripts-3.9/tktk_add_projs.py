#!python

import argparse
import numpy as np
import itk
import os


def main():
    print(args)

    out = None

    for angle in range(args.n):
        file_angle = (args.inputs).replace("%d", f'{angle}')
        if os.path.isfile(file_angle):
            img = itk.imread(file_angle)
            arr = itk.array_from_image(img)
            if out is not None:
                out += arr
            else:
                out = arr

            print(angle)
    out_img = itk.image_from_array(out)
    out_img.CopyInformation(img)
    itk.imwrite(out_img, args.output)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputs")
    parser.add_argument("-n", type=int)
    parser.add_argument("--output")
    args = parser.parse_args()

    main()
