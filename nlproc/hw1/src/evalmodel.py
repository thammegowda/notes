import sys
import os
import numpy as np
import copy
from collections import defaultdict

def confusion_matrix(report, labels):
    n = len(labels)
    table = np.zeros(shape=(n,n))
    lookup = dict((l, i) for i, l in enumerate(labels))
    with open(report, 'r') as f:
        for line in f:
            pred_label, path = line.split()
            act_label = None
            if path.endswith('.spam.txt'):
                act_label = 'spam'
            elif path.endswith('.ham.txt'):
                act_label = 'ham'
            else:
                raise Exception('Cant detect the label from path %s' % path)
            table[lookup[act_label]][lookup[pred_label]] += 1
        return table

def print_matrix(matrix, labels):
    from pprint import pprint
    print(labels)
    pprint(matrix)

def main(report):
    labels = ['spam', 'ham']
    matrix = confusion_matrix(report, labels)
    print_matrix(matrix, labels)

if __name__ == '__main__':
    main(sys.argv[1])
