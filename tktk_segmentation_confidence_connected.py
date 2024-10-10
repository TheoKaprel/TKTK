#!/usr/bin/env python3

import argparse

import itk


def main():
    print(args)

    spect_img = itk.imread(args.spect)
    seed = args.id

    input_type = itk.Image[itk.F, 3]
    output_type = itk.Image[itk.UC, 3]
    confidence = itk.ConfidenceConnectedImageFilter[input_type, output_type].New(
        Input=spect_img,
        Seed=seed,
        NumberOfIterations=5,
        Multiplier=3,
        InitialNeighborhoodRadius=8,
        ReplaceValue=5,
    )
    confidence.Update()
    itk.imwrite(confidence.GetOutput(), args.output)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--spect")
    parser.add_argument("--id", type=int, nargs="+", help = "index of the desired center")
    parser.add_argument("--output")
    args = parser.parse_args()

    main()
