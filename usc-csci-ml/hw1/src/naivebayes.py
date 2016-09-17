from __future__ import print_function
import sys
import os
import numpy as np
import math

class NBModel(object):

    def populate(self, train_X, train_Y):
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
        return self

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
    return np.loadtxt(path, delimiter=',')

def train(csv_db_path):
    train_data = read_dataset(csv_db_path)
    # Skip the id column (0th column), label column (last column)
    train_X = train_data[:, 1:-1]
    train_Y = train_data[:, -1].astype(int)
    return NBModel().populate(train_X, train_Y)

def test(model, csv_db_path):
    test_data = read_dataset(csv_db_path)
    test_X = test_data[:, 1:-1]
    test_Y = test_data[:, -1].astype(int)
    pred_Y = np.array([model.predict(test_X[i]) for i in range(len(test_X))])
    res = np.sum(test_Y == pred_Y)
    return (res * 1.0 / len(test_X))

if __name__ == '__main__':
    if len(sys.argv) != 3:
      print("Error: Invalid args")
      print("Usage: %s <data/train.txt> <data/test.txt>" % sys.argv[0])
      sys.exit(1)
    train_data_path = sys.argv[1]
    test_data_path = sys.argv[2]
    model = train(train_data_path)

    train_acc = test(model, train_data_path)
    test_acc = test(model, test_data_path)
    print(train_acc, test_acc)
    #print("Done")
