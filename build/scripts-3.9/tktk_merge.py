#!python

import argparse
import itk
import numpy as np

def main():
    print(args)

    img1 = itk.imread(args.arg1)
    img2 = itk.imread(args.arg2)

    assert((np.array(img1.GetSpacing())==np.array(img2.GetSpacing())).all())
    assert((np.array(img1.GetOrigin())==np.array(img2.GetOrigin())).all())

    arr1 = itk.array_from_image(img1)
    arr2 = itk.array_from_image(img2)

    arr3 = np.concatenate((arr1,arr2),axis=0)

    img3 = itk.image_from_array(arr3)
    img3.SetSpacing(img1.GetSpacing())

    if args.center:
        size = np.array(itk.size(img3))
        spacing = np.array(itk.spacing(img3))
        centered_origin = [(-size[k] * spacing[k] + spacing[k]) / 2 for k in range(3)]
        img3.SetOrigin(centered_origin)
    else:
        img3.SetOrigin(img1.GetOrigin())

    itk.imwrite(img3, args.output)



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("arg1")
    parser.add_argument("arg2")
    parser.add_argument("--center", action='store_true')
    parser.add_argument("-o","--output")
    args = parser.parse_args()

    main()
