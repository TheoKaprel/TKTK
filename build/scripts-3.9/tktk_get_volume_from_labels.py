#!python

import argparse
import itk
import json
import numpy as np


def main():
    print(args)

    labels_itk = itk.imread(args.imglabel)

    spacing = np.array(labels_itk.GetSpacing())

    volume_voxel = spacing[0]*spacing[1]*spacing[2]
    labels_np = itk.array_from_image(labels_itk)

    print(f'Volume Size : {labels_np.shape}')
    print(f"Volume Spacing : {spacing} (mm)")
    print(f'Voxel volume : {volume_voxel} mm^3')


    if args.label is None:
        l_labels= list(np.unique(labels_np))
    else:
        l_labels=[int(l) for l in args.label]

    print(f"List of labels of interest : {l_labels}")

    for l in l_labels:
        print('---------------')
        npix = (labels_np==l).sum()
        vol = npix * volume_voxel
        print(f'Volume of Label {l} : {round(vol, 3)} mm^3 = {round(vol/1000, 3)} mL')
    print('---------------')



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--imglabel")
    parser.add_argument("-l", "--label", nargs='*', default = None)
    args = parser.parse_args()

    main()
