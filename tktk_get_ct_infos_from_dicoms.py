#!/usr/bin/env python3

import argparse
import pydicom
import matplotlib.pyplot as plt
import numpy as np
from itk import RTK as rtk

def main():
    lmAs,lt,le,lkVp =[], [],[],[]
    for inp in args.inputs:
        ds = pydicom.dcmread(inp)
        lkVp.append(ds[0x18, 0x0060].value)
        lmAs.append(ds[0x18, 0x1151].value)
        lt.append(ds[0x18, 0x1150].value)
        le.append(ds[0x18, 0x1152].value)

    fig,ax =plt.subplots()
    ax.plot(lkVp)
    ax.set_title("kVp")

    fig,ax =plt.subplots()
    ax.plot(lmAs)
    ax.set_title("mAs")

    fig,ax =plt.subplots()
    ax.plot(lt)
    ax.set_title("time (ms)")

    fig,ax =plt.subplots()
    ax.plot(le)
    ax.set_title("exposure")
    print(min(lmAs),max(lmAs))
    plt.show()






if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputs", nargs="*")
    args = parser.parse_args()

    main()
