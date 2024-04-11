#!python

import argparse
import itk
import numpy as np
import glob
import os
import matplotlib.pyplot as plt

def main():
    print(args)

    list_organs = glob.glob(os.path.join(args.segmentation_folder, "*.nii.gz"))

    spect_array = itk.array_from_image(itk.imread(args.spect))

    fig, ax = plt.subplots()

    org_name = []
    org_mean = []
    for org in list_organs:
        name = org.split('/')[1].split('.')[0]
        org_name.append(name)



        org_mask = itk.array_from_image(itk.imread(org))
        mean = (spect_array[org_mask==1]).mean()
        org_mean.append(mean)

    idx = np.argsort(org_mean)
    org_mean_sorted = np.array(org_mean)[idx][::-1]
    org_name_sorted = np.array(org_name)[idx][::-1]

    ax.bar(org_name_sorted, org_mean_sorted)
    plt.xticks(rotation=90)
    plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--segmentation_folder")
    parser.add_argument("--spect")
    args = parser.parse_args()

    main()
