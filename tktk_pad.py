#!/usr/bin/env python3

import argparse
import torch
import itk
import numpy as np


class ZeroPadImgs(torch.nn.Module):
    def __init__(self, size: int) -> None:
        super().__init__()
        self.size = size

    def forward(self, input: torch.Tensor) -> torch.Tensor:
        if input.dim()==3:
            return torch.nn.functional.pad(input, ((self.size - input.shape[2])//2 + (self.size - input.shape[2])%2, (self.size - input.shape[2])//2,
                                               (self.size - input.shape[1])//2 + (self.size - input.shape[1])%2, (self.size - input.shape[1])//2,
                                               (self.size - input.shape[0])//2 + (self.size - input.shape[0])%2, (self.size - input.shape[0])//2),
                                       mode="constant", value=0)
        elif input.dim()==4:
            return torch.nn.functional.pad(input, ((self.size - input.shape[3])//2 + (self.size - input.shape[3])%2, (self.size - input.shape[3])//2,
                                               (self.size - input.shape[2])//2 + (self.size - input.shape[2])%2, (self.size - input.shape[2])//2,
                                               (self.size - input.shape[1])//2 + (self.size - input.shape[1])%2, (self.size - input.shape[1])//2,
                                                   0, 0),
                                           mode="constant", value=0)



def main():
    print(args)
    img = itk.imread(args.input)
    array = itk.array_from_image(img)
    tensor = torch.from_numpy(array)

    pad = ZeroPadImgs(args.padtarget)
    tensor_padded = pad(tensor)
    array_padded = tensor_padded.numpy()
    img_padded = itk.image_from_array(array_padded)
    spacing = np.array(img.GetSpacing())
    img_padded.SetSpacing(spacing)
    origin  = [(-array_padded.shape[k]*spacing[k] + spacing[k])/2 for k in range(3)]
    img_padded.SetOrigin(origin)
    itk.imwrite(img_padded, args.output)
    print(args.output)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--input")
    parser.add_argument("--output")
    parser.add_argument("--padtarget", type = int, default = 112)
    args = parser.parse_args()

    main()
