#!python
import argparse
from math import floor

def main():
    print(args)

    if args.transpose:
        h_out = (args.id - 1)*args.stride - 2*args.padding + (args.kernel-1) + args.output_padding + 1
    else:
        h_out = floor((args.id + 2 * args.padding - (args.kernel -1 ) -1 )/args.stride +1)

    print(f"output dimension = {h_out}")

if __name__ == "__main__":


    # https://pytorch.org/docs/stable/generated/torch.nn.Conv2d.html
    parser = argparse.ArgumentParser(description='''
    From  https://pytorch.org/docs/stable/generated/torch.nn.Conv2d.html\n
    output dimension is computed with the formula : \n,
    
    for conv2d : \n,
    h_out = floor((args.id + 2 * args.padding - (args.kernel -1 ) -1 )/args.stride +1)\n,
    
    for convTranspose2d : 
    
    h_out = (args.id - 1)*args.stride - 2*args.padding + (args.kernel-1) + args.output_padding + 1
    
    ''',)
    parser.add_argument("--id",type=int, help = "input dim")
    parser.add_argument("--kernel", "-k", type=int)
    parser.add_argument("--stride", "-s", type=int)
    parser.add_argument("--padding", "-p", type=int)
    parser.add_argument("--transpose", "-t", action='store_true')
    parser.add_argument("--output_padding",type = int)
    args = parser.parse_args()
    main()
