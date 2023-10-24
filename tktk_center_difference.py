#!/usr/bin/env python3

import argparse
import itk
import numpy as np

def main():
    print(args)
    img1 = itk.imread(args.i1)
    img2 = itk.imread(args.i2)


    size1 = np.array(itk.size(img1))
    size2 = np.array(itk.size(img2))

    spacing1=np.array(img1.GetSpacing())
    spacing2=np.array(img2.GetSpacing())

    origin1=np.array(img1.GetOrigin())
    origin2=np.array(img2.GetOrigin())

    center1 = -(size1-1)*spacing1/2
    center2 = -(size2-1)*spacing2/2
    print("-----------")
    print("img1: ")
    print(f"Size : {size1}")
    print(f"Spacing : {spacing1}")
    print(f"Origin : {origin1}")
    print(f"Center : {center1}")

    print("-----------")
    print("img2: ")
    print(f"Size : {size2}")
    print(f"Spacing : {spacing2}")
    print(f"Origin : {origin2}")
    print(f"Center : {center2}")

    print("-----------")
    print(f"DIFFERENCE : {(origin2-center2) - (origin1-center1)}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--i1")
    parser.add_argument("--i2")
    args = parser.parse_args()

    main()
