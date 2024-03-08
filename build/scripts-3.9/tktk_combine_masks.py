#!python

import argparse
import itk
import numpy as np
import os
import json

def combine(masks, labels, like, output_mask, output_labels):


    like = itk.imread(like)
    like_array = itk.array_from_image(like)
    combined_mask_array = np.zeros_like(like_array)

    dict_organs_labels = {}

    for (mask_fn,label) in zip(masks, labels):
        mask_array = itk.array_from_image(itk.imread(mask_fn))

        label_organ = os.path.basename(mask_fn).split('.nii')[0]
        print(f'Adding organ {label_organ} with label {label}')

        combined_mask_array[mask_array == 1] = label
        dict_organs_labels[label_organ] = label

    combined_mask = itk.image_from_array(combined_mask_array)
    combined_mask.CopyInformation(like)
    itk.imwrite(combined_mask,output_mask)

    formatted_dict_organs_labels = json.dumps(dict_organs_labels, indent=4)
    jsonfile = open(output_labels, "w")
    jsonfile.write(formatted_dict_organs_labels)
    jsonfile.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--masks",type=str, nargs='+')
    parser.add_argument("--labels",type=int, nargs='+')
    parser.add_argument("--like",type=str)
    parser.add_argument("--output_mask",type=str)
    parser.add_argument("--output_labels", type=str)
    args = parser.parse_args()
    print(args)
    combine(masks=args.masks, labels=args.labels, like = args.like, output_mask=args.output_mask, output_labels=args.output_labels)

