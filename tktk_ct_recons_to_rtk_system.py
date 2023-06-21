#!/usr/bin/env python3

import argparse
import itk
import gatetools
import numpy as np
import tktk_ct_to_attmap
import os

def main():
    print(args)

    ct_extension = args.ct[-4:]
    ct_img = itk.imread(args.ct)
    ct_rotated = gatetools.affine_transform.applyTransformation(input=ct_img,keep_original_canvas=True,rotation=[-90,0,0], pad=-1000)

    recons_extension = args.ct[-4:]
    recons_img = itk.imread(args.recons)
    recons_rotated = gatetools.affine_transform.applyTransformation(input=recons_img,keep_original_canvas=True,rotation=[-90,0,0], pad=0)

    recons_rotated_size = np.array(itk.size(recons_rotated))
    recons_rotated_spacing = np.array(itk.spacing(recons_rotated))
    initial_origin = np.array(recons_rotated.GetOrigin())
    output_origin = np.array([(-recons_rotated_size[k]*recons_rotated_spacing[k] + recons_rotated_spacing[k])/2 for k in range(3)])
    identity_direction = np.eye(3)
    recons_rotated.SetOrigin(output_origin)
    recons_rotated.SetDirection(identity_direction)

    ct_origin = np.array(ct_rotated.GetOrigin())
    ct_new_origin = ct_origin+output_origin-initial_origin
    ct_rotated.SetOrigin(ct_new_origin)
    ct_rotated.SetDirection(identity_direction)

    itk.imwrite(recons_rotated, args.recons.replace(recons_extension, '_rtk'+recons_extension))
    ct_rotated_fn = args.ct.replace(ct_extension, '_rtk'+ct_extension)
    itk.imwrite(ct_rotated, ct_rotated_fn)

    dir = os.path.dirname(os.path.realpath(ct_rotated_fn))
    attmap_fn = os.path.join(dir,'attmap.mhd')
    tktk_ct_to_attmap.convert_ct_to_attmap(ct=ct_rotated_fn,output_attmap_fn=attmap_fn,radionuclide='Tc99m')

    attmap = itk.imread(attmap_fn)
    newsize = recons_rotated.GetLargestPossibleRegion().GetSize()
    newspacing = recons_rotated.GetSpacing()
    neworigin = output_origin
    attmap_rtk = gatetools.affine_transform.applyTransformation(input=attmap,
                                                                newsize=newsize, neworigin=neworigin, newspacing=newspacing,
                                                                force_resample=True,pad=0)
    itk.imwrite(attmap_rtk,attmap_fn.replace('.mhd', '_rtk.mhd'))



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--ct")
    parser.add_argument("--recons", help = 'recons image given by constructor')
    args = parser.parse_args()

    main()
