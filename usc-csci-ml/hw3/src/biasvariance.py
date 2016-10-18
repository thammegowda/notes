# Author     : ThammeGowda Narayanaswamy
# Email      : tnarayan@usc.edu
# Student ID : 2074669439
# Subject    : CSCI 567 Fall 16 Homework 3
# Date       : Oct 17, 2016

from __future__ import print_function
import random
import numpy as np
from matplotlib import pyplot as plt
import math
try:
    import matplotlib
    matplotlib.use('TkAgg')
except Exception as e:
    print(e)

# Generate random data
def uniform_randoms(start, end, count):
    return [random.uniform(start, end) for _ in range(count)]

def generate_datasets(start, end, count, sets):
    return np.array([uniform_randoms(start, end, count) for _ in range(sets)])

# define f(x)
def f(x, e=None):
    if e is None:
        e = random.gauss(0.0, math.sqrt(0.1))
    return 2 * x * x + e

def generate_ys(datasets):
    yss = []
    for xs in datasets:
        ys =[f(x) for x in xs]
        yss.append(ys)
    return np.array(yss)

def predict(X, W):
    return np.matmul(X, W)

def MSECost(Y2, Y1):
    return float(np.sum((Y2 - Y1) ** 2) / len(Y2))

def fit_line(X, Y):
    return np.matmul(
        np.matmul(
            np.linalg.pinv(np.matmul(X.transpose(), X)),
            X.transpose()),
        Y)

class LinearRegression(object):

    def __init__(self, X, Y):
        self.means = X.mean(axis=0)
        self.stds = X.std(axis=0)
        X = self.normalize(X)
        self.W = self._find_W(X, Y)

    def _find_W(self, X, Y):
        return fit_line(X, Y)

    def normalize(self, X, standardize=False):
        if standardize:
            X = (X - self.means) / self.stds
        # Bias is added as a weight to simplify the calculations
        X = np.insert(X, 0, 1, axis=1)
        return X

    def predict(self, X):
        X = self.normalize(X)
        return np.matmul(X, self.W)

    def __repr__(self):
        return "W:%s, means:%s, Stds:%s" % (self.W, self.means, self.stds)

def phi(X, high, low=1):
    phi_X = np.zeros(shape=(len(X), 0))
    for power in range(low, high+1):
        phi_X = np.insert(phi_X, phi_X.shape[1], X ** power, axis=1)
    return phi_X

def report_model_complexity(n, num_ds, m=1000):
    highest_poly_deg = 4
    print("Number of datasets=%d, Number of Samples=%d, number of samples in testset:%d" % (num_ds, n, m))
    print("Function\t Variance\t\t Bias^2")
    datasets = generate_datasets(-1, 1, n, num_ds)
    test_set = generate_datasets(-1, 1, m, 1)[0]
    yss = generate_ys(datasets)
    test_ys = generate_ys([test_set])[0]

    fig = plt.figure(1, figsize=(14, 9))
    fig.canvas.set_window_title('Number of DataPoints %d' % n)


    # G1 is a constant output function, no learning required, thus no regression
    predY = np.array([1.0 for _ in range(m)])
    cost = MSECost(test_ys, predY)
    costs = np.array([cost for _ in range(num_ds)]) # all of them have same cost
    variance = 0 #
    bias_2 = np.sum((predY - test_ys)**2) / m
    print("g1\t\t %.8f\t\t %.8f" % (variance, bias_2))
    plt.subplot(2, 3, 1)
    plt.hist(costs, 10, facecolor='green', alpha=0.75)
    plt.xlabel('Sum of Squared Errors')
    plt.ylabel('No of Datasets')
    plt.title(r'$g_%d(x)=1$  $\mu=%f, \sigma=%f$.' % (1, costs.mean(), costs.std()))

    #print("Xs:",datasets)
    for j in range(highest_poly_deg + 1): # highest power of X
        models = [LinearRegression(phi(datasets[i], j), yss[i]) for i in range(num_ds)]
        phi_test_set = phi(test_set, j)
        preds = np.zeros(shape=(num_ds, m))
        costs = np.zeros(num_ds)
        for row in range(num_ds):
            pred_y = models[row].predict(phi_test_set)
            costs[row] = MSECost(pred_y, test_ys)
            for col in range(m):
                preds[row,col] = pred_y[col]

        avgx = preds.mean(axis=0) # averaging over datasets, axis=0 is data_sets
        spread = np.zeros(shape=(num_ds, m))
        for col in range(m):
            for row in range(num_ds):
                spread[row, col] = abs(preds[row,col] - avgx[col])
        variance = np.sum(spread ** 2) / (float(num_ds * m))

        bias_2 = 0.
        for col in range(m):
            bias_2 += (avgx[col] - test_ys[col]) ** 2
        bias_2 = bias_2 / m

        print("%s\t\t %.8f\t\t %.8f" % ("g%d" % (j+2), variance, bias_2))

        #print(costs)
        plt.subplot(2, 3, 2 + j)
        plt.hist(costs, 10, facecolor='green', alpha=0.75)
        plt.xlabel('Sum of Squared Errors')
        plt.ylabel('No of Datasets')
        plt.title(r'$g_%d(x)$  $\mu=%f, \sigma=%f$.' % (j + 2, costs.mean(), costs.std()))

    plt.show()

## Ridge regression
def fit_line_with_bias(X, Y, lambd):
    # (X'X + \lambda I)^{-1} X'Y
    res = np.matmul(X.transpose(), X)
    bias = np.multiply(np.eye(res.shape[0]), lambd)
    res = res + bias
    res = np.linalg.pinv(res)
    res = np.matmul(res, X.transpose())
    res = np.matmul(res, np.array(Y))
    return res

class RidgeRegression(LinearRegression):
    def __init__(self, X, Y, lambd):
        self.lambd = lambd
        super(RidgeRegression, self).__init__(X, Y)

    def _find_W(self, X, Y):
        return fit_line_with_bias(X, Y, self.lambd)

def report_lambd_effect(n, num_ds):
    j = 2 # degree of polynomial
    print("Ridge regression with 2nd degree polynomial")
    Xs = generate_datasets(-1, 1, n, num_ds)
    Ys = generate_ys(Xs)
    m = 100 # samples for test data
    test_set = generate_datasets(-1, 1, m, 1)[0]
    test_ys = generate_ys([test_set])[0]
    lambds = [0.001, 0.003, 0.01, 0.03, 0.1, 0.3, 1.0]

    print("Lambda\t Variance\t Bias")
    for lambd in lambds:
        models = [RidgeRegression(phi(Xs[i], j), Ys[i], lambd) for i in range(num_ds)]
        phi_test_set = phi(test_set, j)
        preds = np.zeros(shape=(num_ds, m))
        for row in range(num_ds):
            pred_y = models[row].predict(phi_test_set)
            for col in range(m):
                preds[row,col] = pred_y[col]

        avgx = preds.mean(axis=0) # averaging over datasets, axis=0 is data_sets
        spread = np.zeros(shape=(num_ds, m))
        for col in range(m):
            for row in range(num_ds):
                spread[row, col] = abs(preds[row,col] - avgx[col])
        variance = np.sum(spread ** 2) / (float(num_ds * m))

        bias_2 = 0.
        for col in range(m):
            bias_2 += (avgx[col] - test_ys[col])**2
        bias_2 = bias_2 / (m)
        print("%g\t %g\t %g" % (lambd, variance, bias_2))

def main():
    report_model_complexity(n=10, num_ds=100, m=100)
    report_model_complexity(n=100, num_ds=100, m=100)
    report_lambd_effect(100, 100)

if __name__ == '__main__':
    main()
