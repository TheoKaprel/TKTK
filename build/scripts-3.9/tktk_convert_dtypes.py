#!python

import argparse
import numpy as np

def get_dtype(opt_dtype):
    if opt_dtype=='float64':
        return np.float64
    elif opt_dtype=='float32':
        return np.float32
    elif opt_dtype=='float16' or opt_dtype=='half':
        return np.float16
    elif opt_dtype=='uint16':
        return np.uint16
    elif opt_dtype=='uint64' or opt_dtype=='uint':
        return np.uint

def main():
    print(args)

    opt_dtype = get_dtype(args.dtype)

    for i in args.inputs:
        print(i)
        arr_old = np.load(i)
        arr_new = arr_old.astype(opt_dtype)
        np.save(i, arr_new)

    print("done!")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputs", nargs='*')
    parser.add_argument("--dtype", choices=['float64', 'float32', 'float16', 'uint16', 'uint64', 'uint'])
    args = parser.parse_args()

    main()
