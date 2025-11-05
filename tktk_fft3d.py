#!/usr/bin/env python3

import argparse
import numpy as np
import itk

def main():
    print(args)
    itk_img = itk.imread(args.input)
    array = itk.array_from_image(itk_img)

    fft_array = np.fft.fftn(array)
    fft_abs_img = np.log(np.abs(np.fft.fftshift(fft_array)) ** 2)
    fft_img = itk.image_from_array(fft_abs_img)
    itk.imwrite(fft_img, args.output)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--input")
    parser.add_argument("--output")
    args = parser.parse_args()

    main()
