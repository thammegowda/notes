# Author     : ThammeGowda Narayanaswamy
# Email      : tnarayan@usc.edu
# Student ID : 2074669439
# Subject    : Naive Bayes Classifier (continuous features) implementation
#              for CSCI 577 Fall 16 Homework 1
# Date       : September 17, 2016

from __future__ import print_function
import sys
import os
import numpy as np
import math

class NBModel(object):

    def __init__(self, train_X, train_Y):
        assert len(train_X) == len(train_Y)
        self.labels = set(train_Y)
        self.n_attrs = train_X.shape[1] # number of columns
        total = train_X.shape[0] # number of rows
        self.prob_l = {}
        self.kb = {}
        for l in self.labels:
            self.kb[l] = {'mean':[], 'var':[]}
            train_lX = train_X[train_Y == l]
            self.prob_l[l] = len(train_lX) / float(total)
            # Compute mean, variance for each attribute i

            means, variances = [], []
            for i in range(self.n_attrs):
                lXi = train_lX[:, i] # Label 'l' attribute 'i'th  X vector
                # Mean = sum/N
                mean = np.sum(lXi) / len(lXi)
                # Variance = SquaredDifference/(N-1)
                variance = np.sum((lXi - mean)**2) / (len(lXi) - 1)
                self.kb[l]['mean'].append(mean)
                self.kb[l]['var'].append(variance)

    def predict(self, new_X):
        assert self.n_attrs == len(new_X)
        preds = {}
        for l in self.labels:
            means = self.kb[l]['mean']
            variances = self.kb[l]['var']
            '''
                P(l | new_X) = P(l) . P(new_X|l)
                               -----------------
                                P(new_X)
                # Here we ignore the denominator, since it is same for all labels, it doesnt affect comparison
                        ~= P(l) . P(new_X1|l) . P(new_X2|l) ... P(new_Xn|l)
                # taking log, whole expression convert into summation

                P(x1|l) =   1 / (sqrt(2.pi.var)) . e^( - (x1 - mean)^2 / (2.var))
                log(p(x1/l)) = -log(sqrt(2.pi.var)) - (x1 - mean)^2 / (2.var)
            '''
            prob = 0
            # prob of label or class
            prob += math.log(self.prob_l[l])
            for i, x in enumerate(new_X):
                # TODO: FIXME: some variances are wrong here
                if np.isclose(0, variances[i]):
                    continue
                prob -= math.log(math.sqrt(2 * math.pi * variances[i]))
                prob -= ((x - means[i]) ** 2) / (2 * variances[i])
            preds[l] = prob
        #print(preds)
        return max(preds, key=preds.get)

def read_dataset(path):
    data = np.loadtxt(path, delimiter=',')
    X = data[:, 1:-1]
    Y = data[:, -1].astype(int)
    return X, Y


def test(model, csv_db_path):
    test_X, test_Y = read_dataset(csv_db_path)
    pred_Y = np.array([model.predict(test_X[i]) for i in range(len(test_X))])
    res = np.sum(test_Y == pred_Y)
    return (res * 1.0 / len(test_X))

def main(train_data_path, test_data_path):
    train_X, train_Y = read_dataset(train_data_path)
    model = NBModel(train_X, train_Y)
    print("#Training data")
    train_acc = test(model, train_data_path)
    print("  Accuracy = %f" % train_acc)

    print("#Testing data")
    test_acc = test(model, test_data_path)
    print("  Accuracy = %f" % test_acc)

if __name__ == '__main__':
    print(sys.argv[1], sys.argv[2])
