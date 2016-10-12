# Topic      : USC CSCI 544 Applied NLP Fall 16 - HW2
#             - Perceptron Classifier for Spam-Ham classification
# Author     : Thamme Gowda Narayanaswamy
# Student ID : 2074-6694-39
# Email      : tnarayan@usc.edu
# Date       : Oct 12, 2016
import os
import sys
import math
import pickle
import logging as log
from random import shuffle
log.basicConfig(level=log.DEBUG)
from collections import defaultdict

ENCODING = 'latin-1'

def scan_data(root):
    for root, dirs, files in os.walk(root):
        label = None
        for name in files:
            if name.startswith('.'):
                continue # skip hidden
            if name.endswith('spam.txt'):
                label = 1
            elif name.endswith('ham.txt'):
                label = -1
            yield label, os.path.join(root, name)

class StdPerceptron(object):

    def __init__(self):
        self.W = defaultdict(int)
        self.bias = 0
        self.count = 0

    def learn(self, data, iters=1):
        for i in range(iters):
            shuffle(data)
            for label, path in data:
                if label is None:
                    raise('Error: No label for %s' % label)
                self.count += 1
                vect = self.vectorize(path)
                pred = self.predict(vect)
                if pred * label <= 0:
                    self.update(vect, label)
            print("Training Epoch %d completed" % (i+1))

    def vectorize(self, path):
        with open(path, 'r', encoding=ENCODING) as f:
            toks = self.tokenize(f.read())
            vect = defaultdict(int) # sparse vector using dict
            for tok in toks:
                vect[tok] += 1
            return vect

    def predict(self, vect):
        val = self.bias
        for k, v in vect.items():
            val += self.W[k] * v
        return val

    def update(self, vect, label):
        self.bias += label
        for k, v in vect.items():
            self.W[k] += v * label

    def tokenize(self, text, unigrams=True, bigrams=False):
        tokens = []
        unigrams = text.split()
        if unigrams:
            tokens.extend(unigrams)
        if bigrams:
            for i in range(0, len(unigrams) - 1):
                tokens.append("%s %s" % (unigrams[i], unigrams[i+1]))
        return tokens

    def save_to_path(self, model_path):
        print('Storing the model at %s' % model_path)
        with open(model_path, 'wb') as f:
            pickle.dump(self, f)
            print('Stored the model at %s' % model_path)

    @staticmethod
    def load_from_path(model_path):
        print('Loading the model from %s' % model_path)
        with open(model_path, 'rb') as f:
            return pickle.load(f)

class AvgPerceptron(StdPerceptron):

    def __init__(self):
        super(AvgPerceptron, self).__init__()
        self.U = defaultdict(int)
        self.beta = 0

    def learn(self, data, iters=1):
        super(AvgPerceptron, self).learn(data, iters)
        # update W from average
        for k, v in self.U.items():
            self.W[k] -= float(self.U[k]) / self.count
        self.bias -= float(self.beta) / self.count

    def update(self, vect, label):
        super(AvgPerceptron, self).update(vect, label)
        # update sum totals
        self.beta += label * self.count
        for k, v in vect.items():
            self.U[k] += v * label * self.count
