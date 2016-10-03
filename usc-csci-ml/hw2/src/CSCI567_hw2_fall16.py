# Author     : ThammeGowda Narayanaswamy
# Email      : tnarayan@usc.edu
# Student ID : 2074669439
# Subject    : CSCI 567 Fall 16 Homework 2
# Date       : Oct 2, 2016

from __future__ import print_function
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

quiet = True # to disable unwanted output
def log(*args):
    if not quiet:
        print(args)

### Global Parameters
alpha = 0.001     # learning rate
conv_tol = 0.05
num_iter = 50000
print_interval = 500
print("The following parameters will be used for gradient descent optimizer:")
print("\t Learning rate=", alpha)
print("\t Convergence Tolerance=", conv_tol)
print("\t Max Iterations=", num_iter)
###

from sklearn.datasets import load_boston
boston = load_boston()
dfX = boston.data
dfY = np.array([boston.target]).transpose()
assert dfX.shape[0] == dfY.shape[0]


test_split_rule = np.arange(dfX.shape[0], dtype=int) % 7 == 0
testX, testY = dfX[test_split_rule], dfY[test_split_rule]
trainX, trainY = dfX[~test_split_rule], dfY[~test_split_rule]

print("##### 3.1 DATA ANALYSIS / EXPLORATION ")
print('Feature Names:\n', pd.DataFrame(boston.feature_names))
print('Dataset shape:', dfX.shape, dfY.shape)
print('Test shape:', testX.shape, testY.shape)
print('Train shape:', trainX.shape, trainY.shape)

n_attrs = trainX.shape[1]
attrs = [trainX[:, i] for i in range(n_attrs)]
stds = [a.std() for a in attrs]
corrs = np.zeros(shape=(n_attrs, n_attrs))
for i, a in enumerate(attrs):
    for j in range(0, i + 1):
        b = attrs[j]
        res = np.cov(a, b) / (stds[i] * stds[j])
        corrs[i][j] = res[0,1]

print("Correlations between the attributes:")
print(pd.DataFrame(corrs))

def pearson_cor(X, Y, names):
    Y = Y[:, 0]
    assert X.shape[0] == Y.shape[0]
    assert X.shape[1] == len(names)
    y_std = Y.std()
    cor = []
    for i in range(X.shape[1]): # each column
        attr = trainX[:, i]
        # Correlation between the attribs and target value
        cor_ab = np.cov(attr, Y) / (stds[i] * y_std)
        cor_ab = abs(cor_ab[0,1])
        cor.append((names[i], cor_ab))
    return cor

def show_plots():
    plt.imshow(corrs, cmap='hot', interpolation='nearest')
    plt.title("Heatmap of correlation between attributes")
    plt.show()
    for i, cor_ab in enumerate(pearson_cor(trainX, trainY, boston.feature_names)):
        print(cor_ab)

    print("##### Generating Histograms")
    bins = 10
    plt.hist(trainY, bins=bins)
    plt.title("Histogram of Price with %d bins" % bins)
    plt.show()

    for i, attr in enumerate(attrs):
        plt.hist(attr, bins=bins)
        plt.title("Histogram of '%s' with %d bins" % (boston.feature_names[i], bins))
        plt.show()

show_plots()

print("\n\n###### 3.2 a LINEAR REGRESSION ALGORITHM")
## Linear Regression

def predict(X, W):
    return np.matmul(X, W)

def MSECost(Y2, Y1):
    # Cost      = 1/N  SIGMA[(XW-Y)^2]
    return float(np.sum((Y2 - Y1) ** 2) / len(Y2))

def gradient_desc(X, Y, W, alpha,
                  num_iter = num_iter, conv_tol=conv_tol, print_interval = print_interval):
    c = float('inf')
    log("Learn Rate", alpha)
    for i in range(num_iter):
        #
        # delta =  2/N SIGMA[(XW - Y)*x]
        predY = predict(X, W)
        diff = predY - Y
        delta = np.sum(np.multiply(X, diff), axis=0) # sum top to bottom for each attribute
        delta  = delta * 2.0 / len(Y)
        delta = np.array([delta]).transpose()        # restore vector shape of (n_attr x 1)

        W = (W - alpha * delta)
        if i % print_interval == 0:
            predY = predict(X, W)
            newcost = MSECost(predY, Y)
            log("#%d, cost = %.8g" % (i, newcost))
            if np.isnan(newcost) or np.isinf(newcost) or np.isneginf(newcost):
                raise Exception("ERROR: number overflow, please adjust learning rate")
            diff = abs(newcost - c)
            c = newcost
            if diff < conv_tol:
                log("Converged with tolerance %f " % conv_tol)
                break
        if i % (print_interval * 10) == 0:
            log(W.flatten())
    return W

# compute means and stds
class LinearRegression(object):

    def __init__(self, X, Y, learn_rate=0.001, num_iter=10000, conv_tol=0.01):

        self.means = X.mean(axis=0)
        self.stds = X.std(axis=0)
        X = self.normalize(X)
        self.n_attrs = X.shape[1]
        W = np.random.rand(self.n_attrs, 1)
        self.W = gradient_desc(X, Y, W, alpha=learn_rate,
                                num_iter=num_iter, conv_tol=conv_tol)

    def normalize(self, X):
        X = (X - self.means) / self.stds
        # Bias is added as a weight to simplify the calculations
        X = np.insert(X, 0, 1, axis=1)
        return X

    def predict(self, X, normalize=True):
        if normalize:
            X = self.normalize(X)
        return np.matmul(X, self.W)

linreg = LinearRegression(trainX, trainY, alpha, num_iter, conv_tol)
print("Gradient Desc Optimization Finished.\nW=", linreg.W.flatten())
predY = linreg.predict(trainX)
train_mse_cost = MSECost(predY, trainY)
test_mse_cost = MSECost(linreg.predict(testX), testY)
print('Train MSE::', train_mse_cost, '\tTest MSE::', test_mse_cost)

######################
print("\n\n##### 3.2 b RIDGE REGRESSION########")

def MSECost_ridge(X, W, Y, lambd):
    # Cost      = 1/N  \SIGMA[(XW-Y)^2] + lambd W||_2^2
    predY = predict(X, W)
    cost = float(np.sum((predY - Y) ** 2)) / len(Y)
    cost += lambd * np.sum((W) ** 2)
    return cost

def gradient_desc_ridge(X, Y, W, alpha, lambd,
                  num_iter = 1000, conv_tol=0.01, check_interval = 500):
    c = float('inf')
    log("Learn Rate", alpha)
    for i in range(num_iter):
        #
        # delta =  2/N SIGMA[(XW - Y)*x] + 2 * \lambd * W
        diff = predict(X, W) - Y
        delta = np.sum(np.multiply(X, diff), axis=0) # sum top to bottom for each attribute
        delta = delta * 2.0 / len(Y)
        delta = np.array([delta]).transpose()        # restore vector shape of (n_attr x 1)
        delta  = delta + (2 * lambd * W)           # Vectors addition

        W = (W - alpha * delta)

        if i % check_interval == 0:
            predY = predict(X, W)
            #print(np.concatenate((Y, predY), axis=1))
            newcost = MSECost_ridge(X, W, Y, lambd)

            log("#%d, cost = %.8g" % (i, newcost))
            if np.isnan(newcost) or np.isinf(newcost) or np.isneginf(newcost):
                raise Exception("ERROR: number overflow, please adjust learning rate")
            diff = abs(newcost - c)
            c = newcost
            if diff < conv_tol:
                log("Converged with tolerance %f " % conv_tol)
                break
        if not quiet and i % (check_interval * 10) == 0:
            print(W.flatten())
    return W


class RidgeRegression(LinearRegression):

    def __init__(self, X, Y, learn_rate=0.001, lambd=0.1, num_iter=1000, conv_tol=0.1):

        self.means = X.mean(axis=0)
        self.stds = X.std(axis=0)
        X = self.normalize(X)
        self.n_attrs = X.shape[1]
        W = np.random.rand(self.n_attrs, 1)
        self.lambd = lambd
        self.W = gradient_desc_ridge(X, Y, W, alpha=learn_rate, lambd=lambd,
                                num_iter=num_iter, conv_tol=conv_tol)

    def predict(self, X, normalize=True):
        if normalize:
            X = self.normalize(X)
        return np.matmul(X, self.W)

    def find_cost(self, X, Y, lambd=None, normalize=True):
        if lambd is None:
            lambd = self.lambd
        if normalize:
            X = self.normalize(X)
        predY = self.predict(X, normalize=False)
        return MSECost_ridge(X, self.W, Y, lambd)

lambds = [0.01, 0.1, 1.0]
results = []
print("\nLambda\t\tTrain MSE\t\tTest MSE")
for lambd in lambds:
    ridreg = RidgeRegression(trainX, trainY, alpha, lambd, num_iter, conv_tol)
    train_mse = ridreg.find_cost(trainX, trainY, lambd=lambd)
    test_mse = ridreg.find_cost(testX, testY, lambd=lambd)
    t = (lambd, train_mse, test_mse)
    print("\t\t".join(map(lambda x: str(x), t)))

###########################
# 10 fold validation
print("\n\n###### 3.2 c RIDGE REGRESSION : 10-FOLD CROSS VALIDATION########")
k = 10
def k_fold_cv(X, Y, lambd, k):
    n = len(Y)
    # Shuffle
    shuf_idx = np.random.permutation(n)
    X, Y = X[shuf_idx], Y[shuf_idx]
    assert k > 1 and k <= n
    ss = n / k # split size
    # split
    accuracy = []
    for i in range(k):
        start, end = i * ss, (i + 1) * ss
        if i == k-1 and end < n:
            # anything left over shall go to the last split (if n is not multiple of k)
            end = n

        # ith split is for testing
        test_X, test_Y =  X[start:end], Y[start:end]
        # everything else for training
        train_X = np.delete(X, np.s_[start, end], axis=0)
        train_Y = np.delete(Y, np.s_[start, end], axis=0)
        ridreg = RidgeRegression(train_X, train_Y, alpha, lambd, num_iter, conv_tol)
        acc = ridreg.find_cost(test_X, test_Y)
        accuracy.append(acc)
    return np.array(accuracy).mean()

lambds = [0.0001, 0.001, 0.01, 0.1, 1, 10]
print("\nLambda\t\tTrain MSE\t\tTest MSE")
for lambd in lambds:
    train_mse = k_fold_cv(trainX, trainY, lambd, k)
    ridreg = RidgeRegression(trainX, trainY, alpha, lambd, num_iter, conv_tol)
    test_mse = ridreg.find_cost(testX, testY, lambd=lambd)
    t = (lambd, train_mse, test_mse)
    print("\t\t".join(map(lambda x: str(x), t)))

######################################################
print("\n\n###### 3.3 a FEATURE SELECTION: TOP 4 CORRELATIONS WITH TARGET")
# Top 4 features

top4TrainX = np.zeros(shape=(len(trainY), 0))
top4TestX = np.zeros(shape=(len(testY), 0))
tuples = pearson_cor(trainX, trainY, boston.feature_names)
target_cor = dict(tuples)
top4= sorted(target_cor, key=target_cor.get, reverse=True)[:4]
for k in top4:
    column = np.where(boston.feature_names == k)[0][0]

    x = np.array([trainX[:, column]]).transpose()
    top4TrainX = np.concatenate((top4TrainX, x), axis=1)

    x = np.array([testX[:, column]]).transpose()
    top4TestX = np.concatenate((top4TestX, x), axis=1)

print("Top4 attrs::", top4)
linreg = LinearRegression(top4TrainX, trainY, alpha)
train_mse_cost = MSECost(linreg.predict(top4TrainX), trainY)
test_mse_cost = MSECost(linreg.predict(top4TestX), testY)

print('Train MSE::', train_mse_cost, " Test MSE::", test_mse_cost)

##########
print("\n\n###### 3.3 b FEATURE SELECTION: TOP 4 CORRELATIONS WITH RESIDUAL ERROR")
# top 4 from residual errors

X_train, Y_train = trainX, trainY
X_test, Y_test = testX, testY
names = boston.feature_names

Z_train = np.zeros(shape=(X_train.shape[0], 0))
Z_test = np.zeros(shape=(X_test.shape[0], 0))

pred_Y = None
for i in range(4):

    # first time we use the target, then on we use the Y - predY

    _Y = Y_train if pred_Y is None else np.subtract(Y_train, pred_Y)
    corrs = dict(pearson_cor(X_train, _Y, names))
    top1 = sorted(corrs, key=corrs.get)[-1]
    print("Choosing: ", top1)
    top1_col = names.tolist().index(top1)

    x = np.array([X_train[:, top1_col]]).transpose()
    Z_train = np.concatenate((Z_train, x), axis=1)

    x = np.array([X_test[:, top1_col]]).transpose()
    Z_test = np.concatenate((Z_test, x), axis=1)

    linreg = LinearRegression(Z_train, Y_train, alpha)
    pred_Y = linreg.predict(Z_train)
    train_mse_cost = MSECost(pred_Y, Y_train)
    test_mse_cost = MSECost(linreg.predict(Z_test), Y_test)

    print('Train MSE::', train_mse_cost, " Test MSE::", test_mse_cost)

    # for the next iteration
    X_train = np.delete(X_train, top1_col, axis=1)
    X_test = np.delete(X_test, top1_col, axis=1)
    names = np.delete(names, top1_col)

######################################
print("\n\n###### 3.3 c FEATURE SELECTION: TOP 4 USING BRUTEFORCE")
# Brute force
import itertools

def brute_force_select():
    least_cost = float('inf')
    best_combination = None
    for cols in itertools.combinations(range(trainX.shape[1]), 4):
        Z_train = np.zeros(shape=(X_train.shape[0], 0))
        Z_test = np.zeros(shape=(X_test.shape[0], 0))

        for col in cols:
            x = np.array([trainX[:, col]]).transpose()
            Z_train = np.concatenate((Z_train, x), axis=1)

            x = np.array([testX[:, col]]).transpose()
            Z_test = np.concatenate((Z_test, x), axis=1)

        linreg = LinearRegression(Z_train, Y_train, alpha)
        train_mse_cost = MSECost(linreg.predict(Z_train), Y_train)
        test_mse_cost = MSECost(linreg.predict(Z_test), Y_test)
        if test_mse_cost < least_cost:
            best_combination = cols
            least_cost = test_mse_cost
        # print(cols, 'Train MSE::', train_mse_cost, " Test MSE::", test_mse_cost)
    return best_combination, least_cost

try:
    print("Performing bruteforce feature selection. Hang tight for results or press CTRL+C to skip")
    best_combination, least_cost = brute_force_select()
    print('Best Combination:: ', best_combination, "Least Test Cost::",  least_cost)
except:
    print("Skipping bruteforce selection...")



###############################
print("\n\n###### 3.4 FEATURE EXPANSION")
# Feature Expansion
Z_train = trainX
Z_test = testX

for i in range(n_attrs):
    xi_train = np.array([trainX[:, i]]).transpose()
    xi_test = np.array([testX[:, i]]).transpose()

    for j in range(0, i+1):
        xj_train = np.array([trainX[:, j]]).transpose()
        xj_test = np.array([testX[:, j]]).transpose()

        Z_train = np.concatenate((Z_train, xi_train * xj_train), axis=1)
        Z_test = np.concatenate((Z_test, xi_test * xj_test), axis=1)

print('Train Shape:', Z_train.shape)
print('Test Shape:', Z_test.shape)
linreg = LinearRegression(Z_train, trainY, alpha)
pred_Y = linreg.predict(Z_train)
train_mse_cost = MSECost(pred_Y, trainY)
test_mse_cost = MSECost(linreg.predict(Z_test), testY)

print('Train MSE::', train_mse_cost, " Test MSE::", test_mse_cost)
