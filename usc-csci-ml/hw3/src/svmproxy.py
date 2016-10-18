# Author     : ThammeGowda Narayanaswamy
# Email      : tnarayan@usc.edu
# Student ID : 2074669439
# Subject    : CSCI 567 Fall 16 Homework 3
# Date       : Oct 17, 2016

from scipy import io as scio
import subprocess
from time import time
import re
import numpy as np

LINEAR = 0
POLY = 1
RBF = 2
test_file = 'phishing-test.mat'
train_file = 'phishing-train.mat'
train_data = "train.data"
test_data = "test.data"

def transform_features(X):
    newX = np.zeros(shape=(X.shape[0], 0))
    for i in range(X.shape[1]):
        vals = set(X[:, i])
        if len(vals) == 3: # break into three boolean cols
            for val in vals:
                new_col = map(lambda a: int(a == val), X[:, i])
                newX = np.insert(newX, newX.shape[1], new_col, axis=1)
        elif -1 in vals:
            new_col = map(lambda a: int(a > 0), X[:, i]) # replace -1 with 0
            newX = np.insert(newX, newX.shape[1], new_col, axis=1)
        else:
            newX = np.insert(newX, newX.shape[1], X[:, i], axis=1)
    return newX

def load_data(fn):
    mat = scio.loadmat(train_file)
    Y = mat['label']
    X = mat['features']
    return transform_features(X), Y.flatten()

def store_svm_vectors(X, Y, file_name):
    assert(len(X) == len(Y))
    with open(file_name, 'wb') as f:
        for i in range(len(Y)):
            f.write("%d " % Y[i]) # label
            pairs = map(lambda t: "%d:%d"% t, enumerate(X[i]))
            f.write(" ".join(pairs)) # attributes
            f.write("\n")


def svm_train(kernel, data, verbose=False, model_file='', **args):
    arg_str = " ".join(map(lambda p: '-%s %s' % (str(p[0]), str(p[1])), args.items()))
    cmd = "svm-train -t %d %s %s %s" % (kernel, arg_str, data, model_file)
    if verbose:
        print(cmd)
    t = time()
    res = subprocess.check_output(cmd.split()).split('\n')
    if 'v' in args:
        res = filter(lambda line: 'Accuracy' in line, res)
        return float(re.search("=\s*(\d*(\.\d*)?)%$", res[0].strip()).group(1)), ((time() - t)/ args['v'])
    return None

def svm_predict(data, model, output):
    cmd = "svm-predict %s %s %s" % (data, model, output)
    return subprocess.check_output(cmd.split()).strip()

def find_best_params(train_data):
    best = float('-inf')
    best_params = None
    print("LINEAR KERNEL\n#\t\tC\tAvgTime\t\tAccuracy%")
    Cs = map(lambda x: pow(4, x), range(-6, 3))
    for i,C in enumerate(Cs):
        res, t = svm_train(POLY, train_data, v=3, c=C)
        print("%d\t %11g\t%f\t%.2f"%(i+1, C, t, res))
        if res > best:
            best = res
            best_params = "Linear Kernel, C=%f" % C

    print("POLYNOMIAL KERNEL\n#\t\t C\tDegree\tAvgTime\t\tAccuracy%")
    Cs = map(lambda x: pow(4, x), range(-3, 8))
    degs = [1,2,3]
    ctr = 0
    for C in Cs:
        for deg in degs:
            ctr += 1
            res, t = svm_train(POLY, train_data, v=3, c=C, d=deg)
            print("%d\t %11g\t%d\t%f\t%.2f"%(ctr, C, deg, t, res))
            if res > best:
                best = res
                best_params = "Plynomial Kernel, C=%f, degree=%d" % (C, deg)


    print("RBF KERNEL\n#\t\t C\tGamma\t\tAvgTime\t\tAccuracy%")
    Cs = map(lambda x: pow(4, x), range(-3, 8))
    gammas = map(lambda x: pow(4, x), range(-7, 0))
    ctr = 0
    for C in Cs:
        for gamma in gammas:
            ctr += 1
            res, t = svm_train(RBF, train_data, v=3, c=C, g=gamma)
            print("%d\t %11g\t%f\t%f\t%.2f"%(ctr, C, gamma, t, res))
            if res > best:
                best = res
                best_params = "RBF Kernel, C=%f, gamma=%f" % (C, gamma)

    print("## BEST RESULTS")
    print(best_params)
    print("Best Accuracy: %.2f" % best)

def check_if_exists(cmd):
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    process.wait()
    return process.returncode
    
def tranform_data():
    X, Y = load_data(train_file)
    testX, testY = load_data(test_file)
    store_svm_vectors(X, Y, train_data)
    store_svm_vectors(testX, testY, test_data)

def main():
    if 1 != check_if_exists("svm-train -h"):
        print("This program calls command svm-train. libsvm is currentlty not available")
        print("Please install libsvm using homebrew or apt-get or conda and make it available in $PATH")
        return
    else:
        print("svm-train command available")
    tranform_data()
    find_best_params(train_data)

if __name__ == '__main__':
    main()
