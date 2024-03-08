#!/usr/bin/env python3

import argparse


def main():
    print(args)

    if (args.u1=="cpm/uCi") and (args.u2=="cps/Bq"):
        conv_factor = 60 * 3.7 * 10 ** 4
        print(f"1 {args.u1} = {conv_factor} {args.u2}")
        print(f"1 {args.u2} = {1/conv_factor} {args.u1}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--u1")
    parser.add_argument("--u2")
    args = parser.parse_args()

    main()
