# Topic      : USC CSCI 544 Applied NLP Fall 16 - HW2
#             - Perceptron Classifier for Spam-Ham classification
# Author     : Thamme Gowda Narayanaswamy
# Student ID : 2074-6694-39
# Email      : tnarayan@usc.edu
# Date       : Oct 12, 2016

import sys
import os
from perceptron import AvgPerceptron
from perceptron import scan_data

if __name__ == '__main__':
    train_dir = sys.argv[1]
    data = list(scan_data(train_dir))
    print("Found %d total examples" % len(data))
    model = AvgPerceptron()
    model.learn(data, 30)
    model.save('per_model.txt')
