#!/usr/bin/env python3

import argparse
import itk
import numpy as np
from scipy.ndimage import label


def main():
    print(args)
    img = itk.imread(args.input)
    array = itk.array_from_image(img)

    structure = np.ones((3, 3, 3))
    labeled_volume, num_features = label(array != 0, structure=structure)
    labeled_volume_itk = itk.image_from_array(labeled_volume)
    labeled_volume_itk.CopyInformation(img)
    itk.imwrite(labeled_volume_itk, args.output)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--input")
    parser.add_argument("--output")
    args = parser.parse_args()

    main()
