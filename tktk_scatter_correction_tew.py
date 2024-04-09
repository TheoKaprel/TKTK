#!/usr/bin/env python3

import argparse
import itk
import numpy as np

def main():
    print(args)

    ileft1,ileft2 = [int(i) for i in args.ileft.split(',')]
    ibase1,ibase2 = [int(i) for i in args.ibase.split(',')]
    iright1,iright2 = [int(i) for i in args.iright.split(',')]
    wleft = args.wleft
    wbase = args.wbase
    wright = args.wright


    input = itk.imread(args.input)
    input_array = itk.array_from_image(input)

    left_window_counts = input_array[ileft1:ileft2,:,:]
    base_window_counts = input_array[ibase1:ibase2,:,:]
    right_window_counts = input_array[iright1:iright2,:,:]

    scatter_estimate = (left_window_counts/wleft + right_window_counts/wright) * wbase/2

    primary_estimate = base_window_counts - scatter_estimate

    primary_estimate[primary_estimate<0] = 0

    primary_estimate_itk = itk.image_from_array(primary_estimate)
    spacing = np.array(input.GetSpacing())
    primary_estimate_itk.SetSpacing(spacing)
    origin  = [(-primary_estimate.shape[k]*spacing[k] + spacing[k])/2 for k in range(3)]
    primary_estimate_itk.SetOrigin(origin)
    itk.imwrite(primary_estimate_itk, args.output)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-i","--input", type = str, required = True )
    parser.add_argument("--wleft", type = float, default=8.929980000000004, help = "width of the lower EW")
    parser.add_argument("--wbase", type = float, default=41.67324,help = "width of the primary EW")
    parser.add_argument("--wright", type = float, default=12.063306315789474,help = "width of the upper EW")
    parser.add_argument("--ileft", type = str, default="360,480",help = "indices of the lower EW")
    parser.add_argument("--ipeak",type = str, default="480,600",help = "indices of the primary EW")
    parser.add_argument("--iright", type = str, default="600,720",help = "indices of the upper EW")
    parser.add_argument("-o","--output", type = str, required = True,help = "output filename")
    args = parser.parse_args()

    main()
