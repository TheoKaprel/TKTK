#!/usr/bin/env python3

import argparse
import itk
import numpy as np
import time

def main():
    print(args)

    spect_img = itk.imread(args.spect)
    spect_array = itk.array_from_image(spect_img)
    spacing = np.array(spect_img.GetSpacing())[::-1]
    size = spect_img.shape

    dict_id = {'1': [62, 37, 57],
    '2': [62, 37, 45],
    '3': [52, 37, 39],
    '4': [41, 37, 45],
    '5': [41, 37, 57],
    '6': [52, 37, 63]}
    dict_diams = {'1': 49,
    '2': 40,
    '3': 34,
    '4': 29,
    '5': 25,
    '6': 22}


    bg_array = itk.array_from_image(itk.imread(args.background))
    mean = (spect_array * bg_array).mean()

    # matrix settings
    lspaceX = np.arange(size[0])
    lspaceY = np.arange(size[1])
    lspaceZ = np.arange(size[2])
    X, Y, Z = np.meshgrid(lspaceX, lspaceY, lspaceZ, indexing='ij')

    for sph_id in dict_id.keys():
        center_id = dict_id[sph_id][::-1]
        radius = dict_diams[sph_id]/2

        region = ((((X-center_id[0])*spacing[0]/radius) ** 2 +
                   ((Y-center_id[1])*spacing[1]/radius) ** 2 +
                   ((Z-center_id[2])*spacing[2]/radius) ** 2) < 1).astype(float)


        max = (spect_array*region).max()

        threshold = 1/2 * (mean+max)

        print(f"mean : {mean}")
        print(f"max : {max}")
        print(f"threshold : {threshold}")


        mask = np.zeros_like(spect_img)
        mask_id = np.where(spect_array>threshold)

        mask[mask_id]=1
        mask = mask*region

        if args.sphere:
            N_pix_in_mask = mask.sum()
            print(f"Npix in mask : {N_pix_in_mask}")
            for r in range(1,int(radius)+1):
                region_r = ((((X - center_id[0]) * spacing[0] / r) ** 2 +
                           ((Y - center_id[1]) * spacing[1] / r) ** 2 +
                           ((Z - center_id[2]) * spacing[2] / r) ** 2) < 1).astype(float)
                print(r, (region_r*mask).sum())
                if (region_r*mask).sum()==N_pix_in_mask:
                    break
            mask_itk = itk.image_from_array(region_r)
            mask_itk.CopyInformation(spect_img)
            itk.imwrite(mask_itk, args.output.replace("%d", sph_id).replace(".mhd", "_sphere.mhd"))

        mask_itk = itk.image_from_array(mask)
        mask_itk.CopyInformation(spect_img)
        itk.imwrite(mask_itk, args.output.replace("%d", sph_id))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--spect")
    parser.add_argument("--background")
    parser.add_argument("--sphere", action='store_true')
    parser.add_argument("--output")
    args = parser.parse_args()

    main()
