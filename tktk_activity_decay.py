#!/usr/bin/env python3

import argparse
import numpy as np


def main():
    print(args)
    a0 = args.a0
    dt = args.dt

    if args.radionuclide=='Tc99m':
        t_hl = 21600
    else:
        print("ERROR: Unknown Radionuclide")
        exit(0)

    A = a0 * np.exp(-np.log(2) * dt / t_hl)

    print(f"A(t0+dt) = {A}")



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''Compute the activity after radioactive decay. Outputs A where A=a0 * exp(-ln(2)/t_hl * dt)
    t_hl is the half life (s) of the selected radionuclide''',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--a0", help="activity at t0", type=float)
    parser.add_argument("--dt",help="time (s) ellapsed between t0 and t", type=float)
    parser.add_argument('-rn','--radionuclide',type=str,default = "Tc99m", choices = ['Tc99m', 'lu77'])
    args = parser.parse_args()

    main()
