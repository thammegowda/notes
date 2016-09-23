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
from nblearn import read_training_data

def main(data_dir, model_path, out_path):
    print("Reading data from %s\nReading model from %s\n" \
        "Storing output to %s" % (data_dir, model_path, out_path))
    model = NaiveBayesModel.load_from_path(model_path)
    data = read_training_data(data_dir)
    with open(out_path, 'w', 1, encoding=ENCODING) as outf:
        for label, path in data:
            with open(path, 'r', encoding=ENCODING) as inf:
                doc = inf.read()
            preds = model.predict(doc)
            maxlabel = max(preds, key=preds.get)
            outf.write("%s %s\n" % (maxlabel, path))

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('ERROR: Invalid args.')
        print('Usage: %s path/to/input/train/data' % sys.argv[0])
        sys.exit(1)
    data_dir = sys.argv[1]
    if not os.path.exists(data_dir) or not os.path.isdir(data_dir):
        print('ERROR: Invalid arg %s.' % data_dir)
        print('The argument should be a valid existing directory path')
        sys.exit(2)
    model_path = 'nbmodel.txt'
    out_path = 'nboutput.txt'
    if not os.path.exists(model_path):
        print('Model doesnt exists at %s.' % data_dir)
        sys.exit(3)
    main(data_dir, model_path, out_path)
