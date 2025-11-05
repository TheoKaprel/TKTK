#!/usr/bin/env python3

import argparse
import itk

def main():
    print(args)

    input_img = itk.imread(args.input)
    like_img = itk.imread(args.like)

    input_img.CopyInformation(like_img)
    itk.imwrite(input_img, args.output)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--input")
    parser.add_argument("--like")
    parser.add_argument("--output")
    args = parser.parse_args()

    main()
