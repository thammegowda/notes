# Author     : ThammeGowda Narayanaswamy
# Email      : tnarayan@usc.edu
# Student ID : 2074669439
# Subject    : CSCI 567 Fall 16 Homework 3
# Date       : Oct 17, 2016

from svmproxy import *
import os

#The highest was RBF
#Cross Validation Accuracy = 97.2%
C=256
gamma=0.015625

tranform_data()

model = "best_model.dat"
print("Saving model at %s" % model)
svm_train(RBF, train_data, model_file=model, c=C, g=gamma, verbose=True)
print("Test Accuracy::")
print(svm_predict(test_data, model, "output.txt"))
