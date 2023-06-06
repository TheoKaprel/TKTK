#!/usr/bin/env python3

import argparse
import itk
import numpy as np

def main():
    print(args)

    img = itk.imread(args.input)
    array = itk.array_from_image(img)
    print(array.shape)
    array_splitted1 = array[:args.id,:,:]
    array_splitted2 = array[args.id:,:,:]
    img_splitted1 = itk.image_from_array(array_splitted1)
    img_splitted2 = itk.image_from_array(array_splitted2)
    img_splitted1.SetSpacing(img.GetSpacing())
    img_splitted2.SetSpacing(img.GetSpacing())
    itk.imwrite(img_splitted1, args.outputs[0])
    itk.imwrite(img_splitted2, args.outputs[1])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("id", type = int)
    parser.add_argument("outputs", nargs='*')
    args = parser.parse_args()

    main()
