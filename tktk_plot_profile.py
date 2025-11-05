#!/usr/bin/env python3

import argparse


def main():
    print(args)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("arg1")
    args = parser.parse_args()

    main()
