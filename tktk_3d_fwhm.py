#!/usr/bin/env python3

import argparse
import itk
import numpy as np
from scipy.signal import peak_widths
import matplotlib.pyplot as plt


def main():
    print(args)

    img = itk.imread(args.input)
    array = itk.array_from_image(img)

    if (args.lowercrop is not None) and (args.uppercrop is not None):
        i1,i2,i3=args.lowercrop
        j1,j2,j3=args.uppercrop
        n1,n2,n3 = array.shape
        array = array[i1 : n1 - j1, i2 : n2 - j2, i3 : n3 - j3]

    print(array.shape)

    spacing= np.array(img.GetSpacing())

    max_profile_x = array.sum(axis=(0,1))
    results_half = peak_widths(max_profile_x,[max_profile_x.argmax()], 0.5)
    fwhm_x = results_half[0][0]*spacing

    max_profile_y = array.sum(axis=(0,2))
    results_half = peak_widths(max_profile_y,[max_profile_y.argmax()], 0.5)
    fwhm_y = results_half[0][0]*spacing

    max_profile_z = array.sum(axis=(1,2))
    results_half = peak_widths(max_profile_z,[max_profile_z.argmax()], 0.5)
    fwhm_z = results_half[0][0]*spacing


    print(f'FWHM x : {fwhm_x} mm')
    print(f'FWHM y : {fwhm_y} mm')
    print(f'FWHM z : {fwhm_z} mm')
    print(f' -x {fwhm_x[0]} -y {fwhm_y[0]} -z {fwhm_z[0]}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--input")
    parser.add_argument("--lowercrop", type=int, nargs="+")
    parser.add_argument("--uppercrop", type=int, nargs="+")
    args = parser.parse_args()

    main()
