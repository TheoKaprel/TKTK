#!/usr/bin/env python3

import argparse
import numpy as np
import itk


def main():
    print(args)

    first = itk.imread(args.inputs[0])
    first_np = itk.array_from_image(first)

    ninpts = len(args.inputs)
    nprjs = args.nprojpersubset
    nw = first_np.shape[0] // nprjs
    nx, ny = first_np.shape[1], first_np.shape[2]

    out = np.zeros((nw * nprjs * ninpts, nx, ny))

    for i, img_fn in enumerate(args.inputs):
        print('-----------------------')
        img = itk.imread(img_fn)
        array = itk.array_from_image(img)
        for w in range(nw):
            idw = w * nprjs * ninpts
            for k in range(nprjs):
                print(idw + k * ninpts + i)
                out[idw + k * ninpts + i, :, :] = array[w * nprjs + k, :, :]

    out_img = itk.image_from_array(out)
    itk.imwrite(out_img, args.output)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputs", nargs='+')
    parser.add_argument("--nprojpersubset", type=int)
    parser.add_argument("--output")
    args = parser.parse_args()

    main()

