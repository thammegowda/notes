#!/usr/bin/env python
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import sys
import argparse



def read_input(fp):
    items = []
    for line in sys.stdin:
        line = line.strip()
        items.append(int(line))
    return items


def histogram(items, title='Counts', bins=30, outp=None):
    plt.figure()
    plt.hist(items)
    plt.ylabel(title)
    if outp:
        plt.savefig(outp)
    else:
        plt.show()

def main():
    p = argparse.ArgumentParser()
    p.add_argument('-i', '--inp', type=argparse.FileType('r'),
                   default=sys.stdin, help='Input File having one number per line')
    p.add_argument('-o', '--out', type=str, help='Output file to store image (optional)')
    args = p.parse_args()
    items = read_input(args.inp)
    histogram(items)


if __name__ == '__main__':
    main()

