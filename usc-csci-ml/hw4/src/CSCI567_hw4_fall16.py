# Author     : ThammeGowda Narayanaswamy
# Email      : tnarayan@usc.edu
# Student ID : 2074669439
# Subject    : CSCI 567 Fall 16 Homework 4
# Date       : Oct 27, 2016

# coding: utf-8

from hw_utils import *
from copy import copy

data_path = 'MiniBooNE_PID.txt'

# ## Load Data
## (c)
print("## (c) Loading and Normalizing the dataset")
X_tr, Y_tr, X_te, Y_te = loaddata(data_path)
print "Train X, Y :", X_tr.shape, Y_tr.shape
print "Test  X, Y :", X_te.shape, Y_te.shape
X_tr, X_te = normalize(X_tr, X_te)
d_in = X_tr.shape[1] # input features
d_out = Y_tr.shape[1] # Output predictions

## (d)
# default args
args = {
    'actfn':'linear',
    'last_act':'softmax',
    'reg_coeffs': [0.0],
    'num_epoch': 30,
    'batch_size': 1000,
    'sgd_lr': 0.001,
    'sgd_decays': [0.0],
    'sgd_moms': [0.0],
    'sgd_Nesterov': False,
    'EStop': False,
    'verbose': False
}


# FIXME: BEGIN : This is for quick testing
args['batch_size'] = 10
X_tr, Y_tr = X_tr[:100], Y_tr[:100]
X_te, Y_te = X_te[:100], Y_tr[:100]
print "Train X, Y :", X_tr.shape, Y_tr.shape
# FIXME: END

print("\n\n## (d) Linear Activation ")
archs = [[d_in, d_out],
        [d_in, 50, d_out],
        [d_in, 50, 50, d_out],
        [d_in, 50, 50, 50, d_out]]
testmodels(X_tr, Y_tr, X_te, Y_te, archs, **args)

archs = [[d_in, 50, d_out],
         [d_in, 500, d_out],
         [d_in, 500, 300, d_out],
         [d_in, 800, 500, 300, d_out],
         [d_in, 800, 800, 500, 300, d_out]]
testmodels(X_tr, Y_tr, X_te, Y_te, archs, **args)

# (e)
print("\n\n## (e) Sigmoid Activation")
args['actfn'] = 'sigmoid'
testmodels(X_tr, Y_tr, X_te, Y_te, archs, **args)

# (f)
print("\n\n## (f) ReLu Activation")
args['actfn'] = 'relu'
args['sgd_lr'] = 5e-4
testmodels(X_tr, Y_tr, X_te, Y_te, archs, **args)

# (g)
print("\n\n## (g) Regularization Coefficients")
archs = [[d_in, 800, 500, 300, d_out]]
args['reg_coeffs'] = [1e-7, 5e-7, 1e-6, 5e-6, 1e-5]
best, _ = testmodels(X_tr, Y_tr, X_te, Y_te, archs, **args)
best_lambda_noEstop = best[1]
print("Best Regularization Coefficient=", best_lambda_noEstop)

# (h)
print("\n\n## (h) Regularization Coefficients -- Early stop")
args['EStop'] = True
best, _ = testmodels(X_tr, Y_tr, X_te, Y_te, archs, **args)
best_lambda_EStop = best[1]
print("Best Regularization Coefficient with early stopping=", best_lambda_EStop)

# (i)
print("\n\n## (i) SGD Decay")
args['reg_coeffs'] = [5e-7]
args['num_epoch'] = 100
args['sgd_lr'] = 1e-5
args['sgd_decays'] = [1e-5, 5e-5, 1e-4, 3e-4, 7e-4, 1e-3]
args['EStop'] = False
best, _ = testmodels(X_tr, Y_tr, X_te, Y_te, archs, **args)
best_decay = best[2]
print("Best Decay", best_decay)

# (j)
print("\n\n## (j) SGD Momentum")
args['reg_coeffs'] = [0.0]
args['num_epoch'] = 50
args['sgd_decays'] = [best_decay]
args['sgd_Nesterov'] = True
args['sgd_moms']= [0.99, 0.98, 0.95, 0.9, 0.85]
best, _ = testmodels(X_tr, Y_tr, X_te, Y_te, archs, **args)
best_mom = best[3]
print("Best moemntum", best_mom)

# (k)
print("\n\n## (k) Combining all")
args['num_epoch'] = 100
args['sgd_lr'] = 1e-5
args['sgd_Nesterov'] = True
args['EStop'] = True


args['sgd_decays'] = [best_decay]
args['sgd_moms']= [best_mom]
args['reg_coeffs'] = [best_lambda_EStop]

testmodels(X_tr, Y_tr, X_te, Y_te, archs, **args)

# (l) Grid Search
print("\n\n## (j) Grid Search ")
archs = [[d_in, 50, d_out],
        [d_in, 500, d_out],
        [d_in, 500, 300, d_out],
        [d_in, 800, 500, 300, d_out],
        [d_in, 800, 800, 500, 300, d_out]]
args = {
    'actfn':'relu',
    'last_act':'softmax',
    'num_epoch': 100,
    'batch_size': 1000,
    'sgd_lr': 1e-5,
    'sgd_Nesterov': True,
    'sgd_moms': [0.99],
    'EStop': True,
    'verbose': False,
    'reg_coeffs': [1e-7, 5e-7, 1e-6, 5e-6, 1e-5],
    'sgd_decays': [1e-5, 5e-5, 1e-4],
}
testmodels(X_tr, Y_tr, X_te, Y_te, archs, **args)
