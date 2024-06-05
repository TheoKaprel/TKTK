#!python

import argparse
import numpy as np
import itk
import os


def main():
    print(args)

    out = None

    for i in range(args.n):
        file_i = (args.inputs).replace("%d", f'{i}')
        if os.path.isfile(file_i):
            img = itk.imread(file_i)
            arr = itk.array_from_image(img)
            if out is not None:
                out += arr
            else:
                out = arr
            print(i)
    out_img = itk.image_from_array(out)
    out_img.CopyInformation(img)
    itk.imwrite(out_img, args.output)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputs", help="should contain a pourcent-d to replace with integer")
    parser.add_argument("-n", type=int, help="nb of inputs to add together")
    parser.add_argument("--output", help="otuput filename")
    args = parser.parse_args()

    main()
