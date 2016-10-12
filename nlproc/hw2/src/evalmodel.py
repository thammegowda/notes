# Topic      : USC CSCI 544 Applied NLP Fall 16 - HW2
#             - Perceptron Classifier for Spam-Ham classification
# Author     : Thamme Gowda Narayanaswamy
# Student ID : 2074-6694-39
# Email      : tnarayan@usc.edu
# Date       : Oct 12, 2016
import sys
import os
import numpy as np
import copy
from collections import defaultdict

def get_label_from_path(path):
    if path.endswith('.spam.txt'):
        act_label = 'spam'
    elif path.endswith('.ham.txt'):
        act_label = 'ham'
    else:
        raise Exception('Cant detect the label from path %s' % path)
    return act_label

def confusion_matrix(report, labels):
    n = len(labels)
    table = np.zeros(shape=(n,n))
    lookup = dict((l, i) for i, l in enumerate(labels))
    with open(report, 'r') as f:
        for line in f:
            pred_label, path = line.split()
            act_label = get_label_from_path(path)
            table[lookup[act_label]][lookup[pred_label]] += 1
        return table

def print_matrix(matrix, labels):
    from pprint import pprint
    print(labels)
    pprint(matrix)

def main(report):
    labels = ['spam', 'ham']
    matrix = confusion_matrix(report, labels)
    f1_score = float(np.trace(matrix)) / np.sum(matrix)
    print("Overall Accuracy: is %f" % f1_score)

    actual_count = np.sum(matrix, axis=1)
    preds_count = np.sum(matrix, axis=0)
    print("Label\tPrecision\tRecall\tF1-Score")
    for idx, label in enumerate(labels):
        precision = matrix[idx,idx] / preds_count[idx]
        recall = matrix[idx,idx] / actual_count[idx]
        f1 = 2 * precision * recall / (precision + recall)
        print("%s\t%.2f\t\t%.2f\t%.2f" % (label, precision, recall, f1))

    print("\nCounts:")
    print("*\t", end='')
    for lbl in labels:
        print("\t%s" % lbl, end='')
    print('\tAct.Total')
    for row, rlabel in enumerate(labels):
        print(rlabel, end='\t')
        for col, clabel in enumerate(labels):
            print("\t%d" % matrix[row][col], end='')
        print("\t%d" % actual_count[row])
    print("Pred.Total", end='')
    for idx,lbl in enumerate(labels):
        print("\t%d" % preds_count[idx], end='')
    print("\t%d" % np.sum(actual_count))

if __name__ == '__main__':
    main(sys.argv[1])
