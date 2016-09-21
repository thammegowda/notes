# Author     : ThammeGowda Narayanaswamy
# Email      : tnarayan@usc.edu
# Student ID : 2074669439
# Subject    : K Nearest Neighbor implementation for CSCI 567 Fall 16 Homework 1
# Date       : September 17, 2016

from __future__ import print_function
import numpy as np
import sys
from heapq import heappush as push, heappop as pop

#FIXME: normalize data
def l1_measure(pt1, pt2):
    assert len(pt1) == len(pt2)
    return np.sum(np.absolute(pt1 - pt2))

def l2_measure(pt1, pt2):
    assert len(pt1) == len(pt2)
    return np.sqrt(np.sum((pt1 - pt2)**2))

dist_measures = {"l1": l1_measure, "l2": l2_measure}
Ks = [1, 3, 5, 7]

class KNNModel(object):

    def __init__(self, train_X, train_Y):
        self.means =  np.mean(train_X, axis=0)
        self.stds = np.std(train_X, axis=0)
        self.X = (train_X - self.means) / self.stds     # normalize
        self.Y = train_Y
        self.means = np.mean(train_X, axis=0)
        self.vars = np.var(train_X, axis=0)

    def predict(self, new_X, k, dist_measure):
        assert k > 0
        assert dist_measure in dist_measures
        heap = []
        new_X = (new_X - self.means) / self.stds
        for i in range(len(self.X)):
            dist = dist_measures[dist_measure](self.X[i], new_X)
            push(heap, (dist, i))
        labels = list(map(lambda i: self.Y[pop(heap)[1]], range(k)))
        return np.bincount(labels).argmax()

def read_dataset(path):
    data = np.loadtxt(path, delimiter=',')
    X = data[:, 1:-1]
    Y = data[:, -1].astype(int)
    return X, Y

def test_loo(csv_db_path):
    X, Y  = read_dataset(csv_db_path)
    n = len(X)
    for dist_measure in dist_measures.keys():
        for k in Ks:
            errors = 0
            for i in range(n):
                # Leave one out
                train_X, train_Y = np.delete(X, i, axis=0), np.delete(Y, i)
                # going to predict the left out
                new_x, expct_y = X[i], Y[i]
                model = KNNModel(train_X, train_Y)
                pred_y = model.predict(new_x, k, dist_measure)
                if pred_y != expct_y:
                    errors += 1
            f1_score = float(n - errors) / n
            print("  K=%d, dist_measure=%s, accuracy=%f" % (k, dist_measure, f1_score))

def test(model, csv_db_path):
    test_X, test_Y  = read_dataset(csv_db_path)
    for dist_measure in dist_measures.keys():
        for k in Ks:
            pred_Y = np.array([model.predict(test_X[i], k, dist_measure) \
                for i in range(len(test_X))])
            res = np.sum(test_Y == pred_Y)
            f1_score = res * 1.0 / len(test_X)
            print("  K=%d, dist_measure=%s, accuracy=%f" % (k, dist_measure, f1_score))

def main(train_data_path, test_data_path):
    print("#Training data with Leave one out strategy")
    test_loo(train_data_path)
    print("#Testing data")
    train_X, train_Y = read_dataset(train_data_path)
    model = KNNModel(train_X, train_Y)
    test(model, test_data_path)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
