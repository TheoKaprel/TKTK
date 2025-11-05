#!python

import argparse
import itk
import numpy as np

def main():
    print(args)
    l = []
    for input_fn in args.inputs:
        img = itk.imread(input_fn)
        array = itk.array_from_image(img)
        input_size = np.array(itk.size(img))
        input_spacing = np.array(itk.spacing(img))
        l.append(array)

    merged_array = np.concatenate(l, axis=0)

    merged_img = itk.image_from_array(merged_array)
    merged_img.SetSpacing(input_spacing)
    origin = [(-input_size[k]*input_spacing[k] + input_spacing[k])/2 for k in range(3)]
    merged_img.SetOrigin(origin)
    itk.imwrite(merged_img, args.output)



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputs", nargs="+")
    parser.add_argument("-o","--output")
    args = parser.parse_args()

    main()
