#!/usr/bin/env python3

import argparse
import itk
import numpy as np


def main():
    print(args)

    for image in args.image:
        print('-'*20+'INFORMATIONS AND STATS'+'-'*30)
        print(f'Filename : {image}')

        if (image[-3:]=='mhd') or (image[-3:]=='mha'):
            img = itk.imread(image)
            array=itk.array_from_image(img)
        elif (image[-3:]=='npy'):
            array = np.load(image)
        else:
            print('ERROR: Unrecognized image type')
            exit(0)

        print(f'Size : {array.shape}')
        print(f'Origin : {img.GetOrigin()}')
        print(f'Spacing : {img.GetSpacing()}\n')

        print(f'Mean : {array.mean()}')
        print(f'Sum : {array.sum()}')
        print(f'Min : {array.min()}')
        print(f'Max : {array.max()}')
        print(f'Std : {np.std(array)}')



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("image", nargs='+')
    args = parser.parse_args()

    main()
