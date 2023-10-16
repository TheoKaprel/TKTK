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

    ct_size = np.array(itk.size(ct_img))
    ct_spacing = np.array(itk.spacing(ct_img))
    ct_origin = np.array(itk.origin(ct_img))
    center_0_ct = -(ct_size*ct_spacing - ct_spacing)/2
    center_ct =  ct_origin - center_0_ct

    recons_img_size = np.array(itk.size(recons_img))
    recons_img_spacing = np.array(itk.spacing(recons_img))
    recons_img_origin = np.array(itk.origin(recons_img))
    center_0_rec = -(recons_img_size*recons_img_spacing - recons_img_spacing)/2
    center_recons_img =  recons_img_origin - center_0_rec

    translation = center_recons_img - center_ct
    ct_translated = gatetools.affine_transform.applyTransformation(input=ct_img,translation=translation,pad=-1000, force_resample=True)

    ct_translated.SetOrigin(center_0_ct)
    recons_img.SetOrigin(center_0_rec)

    # itk.imwrite(recons_img, args.recons.replace(recons_extension, '_c' + recons_extension))
    # itk.imwrite(ct_translated, args.ct.replace(ct_extension, '_c' + ct_extension))

    ct_c_rot = gatetools.affine_transform.applyTransformation(input=ct_translated,keep_original_canvas=True,rotation=[-90,0,0], pad=-1000)
    rec_rot = gatetools.affine_transform.applyTransformation(input=recons_img,keep_original_canvas=True,rotation=[-90,0,0], pad=0)

    itk.imwrite(rec_rot, args.recons.replace(recons_extension, '_rtk' + recons_extension))
    itk.imwrite(ct_c_rot, args.ct.replace(ct_extension, '_c_rot' + ct_extension))


    ct_c_rot_resized = gatetools.affine_transform.applyTransformation(input=ct_c_rot,
                                                                newsize=rec_rot.GetLargestPossibleRegion().GetSize(),
                                                                newspacing=rec_rot.GetSpacing(),
                                                                keep_original_canvas=True,pad=-1000)


    dir = os.path.dirname(os.path.realpath(args.ct))
    attmap_fn = os.path.join(dir,'attmap_rtk.mhd')
    attmap = tktk_ct_to_attmap.convert_ct_to_attmap(ctImage=ct_c_rot_resized, radionuclide='Tc99m')
    itk.imwrite(attmap,attmap_fn)





if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--ct")
    parser.add_argument("--recons", help = 'recons image given by constructor')
    args = parser.parse_args()

    main()
