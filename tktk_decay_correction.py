#!/usr/bin/env python3

import argparse
import matplotlib.pyplot as plt
import itk
import numpy as np

def main():
    print(args)
    dt = args.dt
    projs_fn=args.projs

    projs=itk.imread(projs_fn)
    projs_array=itk.array_from_image(projs)
    projs_array_DC = np.zeros_like(projs_array)

    if args.radionuclide=='Tc99m':
        t_hl = 21600
    else:
        print("ERROR: Unknown Radionuclide")
        exit(0)

    # fig,ax = plt.subplots()
    for i in range(120):
        # t_elapsed = (i%60) * dt
        t_elapsed = (i%60) * (dt + 20)
        CF = np.exp(-np.log(2) * t_elapsed / t_hl)
        # ax.scatter(i,CF,c='blue', s=10)
        projs_array_DC[i,:,:] = projs_array[i,:,:]/CF

    projs_DC = itk.image_from_array(projs_array_DC)
    projs_DC.CopyInformation(projs)
    itk.imwrite(projs_DC,args.output)

    # plt.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--projs")
    parser.add_argument("--dt", type=float)
    parser.add_argument('-rn','--radionuclide',type=str,default = "Tc99m", choices = ['Tc99m', 'lu77'])
    parser.add_argument("--output")
    args = parser.parse_args()

    main()
