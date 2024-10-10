#!/usr/bin/env python3

import argparse
import numpy as np
import itk

def main():
    print(args)


    out = None

    for i,inpt in enumerate(args.inputs):
        if out is None:
            img = itk.imread(inpt)
            array = itk.array_from_image(img)

            out = np.zeros((len(args.inputs),array.shape[0], array.shape[1], array.shape[2]))

            out[0,:,:,:] = array[:,:,:]
        else:
            array = itk.array_from_image(itk.imread(inpt))
            out[i,:,:,:]=array

    out_img =itk.image_from_array(out)
    spacing = np.array(img.GetSpacing())
    out_img.SetSpacing([spacing[0], spacing[1], spacing[2], 1])
    origin = np.array(img.GetOrigin())
    origin_ = [origin[0], origin[1], origin[2],(-out.shape[0]+1)/2]
    out_img.SetOrigin(origin_)
    itk.imwrite(out_img, args.output)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputs", nargs="+")
    parser.add_argument("--output")
    args = parser.parse_args()

    main()
