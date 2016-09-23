# Topic      : USC CSCI 544 Applied NLP Fall 16 - HW1
#             - Naive Bayes Classifier for Spam-Ham classification
# Author     : Thamme Gowda Narayanaswamy
# Student ID : 2074-6694-39
# Email      : tnarayan@usc.edu
# Date       : Sept 22, 2016

import sys
import os
from nbmodel import NaiveBayesModel
from nbmodel import ENCODING

def read_training_data(dir):
    for root, dirs, files in os.walk(dir):
        for name in files:
            if name.startswith('.'):
                continue # skip hidden
            if name.endswith('spam.txt'):
                label = 'spam'
            elif name.endswith('ham.txt'):
                label = 'ham'
            yield label, os.path.join(root, name)

def main(train_dir, labels=['spam', 'ham']):
    print('Train dir: %s' % train_dir)
    paths = {}
    for label in labels:
        paths[label] = []
    for label, path in read_training_data(train_dir):
        if label == None:
            print('Label is None for Path=%s' % path)
        paths[label].append(path)

    model = NaiveBayesModel(paths)
    fname = 'nbmodel.txt'
    model.save_to_path(fname)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('ERROR: Invalid args.')
        print('Usage: %s path/to/input/train/data' % sys.argv[0])
        sys.exit(1)
    train_dir = sys.argv[1]
    if not os.path.exists(train_dir) or not os.path.isdir(train_dir):
        print('ERROR: Invalid arg %s.' % train_dir)
        print('The argument should be a valid existing directory path')
        sys.exit(2)
    main(train_dir)
