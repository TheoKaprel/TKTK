#!/usr/bin/env python3

import argparse
import itk
import numpy as np
import torch

def main():
    print(args)

    device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")

    image = itk.imread(args.input)
    image_array = itk.array_from_image(image)
    image_tensor = torch.Tensor(image_array).to(device)

    kernel = itk.imread(args.kernel)
    kernel_tensor = torch.Tensor(itk.array_from_image(kernel)).to(device)



    conv = torch.nn.Conv3d(in_channels=1, out_channels=1, kernel_size=kernel_tensor.shape, stride=(1, 1, 1),
                           padding=((kernel_tensor.shape[0]-1)//2,(kernel_tensor.shape[1]-1)//2,(kernel_tensor.shape[2]-1)//2), bias=False).to(device)

    conv.weight.data = kernel_tensor[None,None,:,:,:]

    output_tensor = conv(image_tensor[None,None,:,:,:])

    output_array = output_tensor.detach().squeeze().cpu().numpy()
    output_image = itk.image_from_array(output_array)
    output_image.CopyInformation(image)
    itk.imwrite(output_image, args.output)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", '-i')
    parser.add_argument("--kernel", '-k')
    parser.add_argument('--output', '-o')
    args = parser.parse_args()

    main()
