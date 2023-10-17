#!/usr/bin/env python3

import argparse
import itk
import gatetools
import numpy as np
import tktk_ct_to_attmap,tktk_center_image
import os

def main():
    print(args)

    ct_extension = args.ct[-4:]
    ct_img = itk.imread(args.ct)
    recons_extension = args.ct[-4:]
    recons_img = itk.imread(args.recons)


    ct_rot = gatetools.affine_transform.applyTransformation(input=ct_img,keep_original_canvas=True,rotation=[-90,0,0], pad=-1000)
    rec_rot = gatetools.affine_transform.applyTransformation(input=recons_img,keep_original_canvas=True,rotation=[-90,0,0], pad=0)

    itk.imwrite(rec_rot, args.recons.replace(recons_extension, '_r' + recons_extension))
    itk.imwrite(ct_rot, args.ct.replace(ct_extension, '_r' + ct_extension))


    ct_rot_resized = gatetools.affine_transform.applyTransformation(input=ct_rot,
                                                                newsize=rec_rot.GetLargestPossibleRegion().GetSize(),
                                                                newspacing=rec_rot.GetSpacing(),
                                                                keep_original_canvas=True,pad=-1000)


    dir = os.path.dirname(os.path.realpath(args.ct))
    attmap_fn = os.path.join(dir,'attmap_rtk.mhd')
    attmap = tktk_ct_to_attmap.convert_ct_to_attmap(ctImage=ct_rot_resized, radionuclide='Tc99m')
    itk.imwrite(attmap,attmap_fn)





if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--ct")
    parser.add_argument("--recons", help = 'recons image given by constructor')
    args = parser.parse_args()

    main()
