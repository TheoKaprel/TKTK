#!/usr/bin/env python3



import argparse
import itk
import gatetools
import numpy as np

def center(input_image):

    input_size = np.array(itk.size(input_image))
    input_spacing = np.array(itk.spacing(input_image))

    output_origin = [(-input_size[k]*input_spacing[k] + input_spacing[k])/2 for k in range(3)]
    output_direction = np.eye(3)

    input_image.SetOrigin(output_origin)
    input_image.SetDirection(output_direction)
    return input_image


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i")
    parser.add_argument("--output", "-o")
    args = parser.parse_args()

    input_image = itk.imread(args.input)
    output_img = center(input_image=input_image)
    itk.imwrite(output_img, args.output)
