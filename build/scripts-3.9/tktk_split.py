#!python

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
    if args.center==True:
        input_spacing1 = np.array(itk.spacing(img_splitted1))
        input_size1 = np.array(itk.size(img_splitted1))
        input_spacing2 = np.array(itk.spacing(img_splitted2))
        input_size2 = np.array(itk.size(img_splitted2))

        output_splitted1_origin = [(-input_size1[k] * input_spacing1[k] + input_spacing1[k]) / 2 for k in range(3)]
        output_splitted2_origin = [(-input_size2[k] * input_spacing2[k] + input_spacing2[k]) / 2 for k in range(3)]
        output_direction = np.eye(3)

        img_splitted1.SetOrigin(output_splitted1_origin)
        img_splitted1.SetDirection(output_direction)

        img_splitted2.SetOrigin(output_splitted2_origin)
        img_splitted2.SetDirection(output_direction)
    else:
        img_splitted1.SetDirection(img.GetDirection())
        img_splitted2.SetDirection(img.GetDirection())

    itk.imwrite(img_splitted1, args.outputs[0])
    itk.imwrite(img_splitted2, args.outputs[1])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("id", type = int)
    parser.add_argument("outputs", nargs='*')
    parser.add_argument("--center", action ="store_true")
    args = parser.parse_args()

    main()
