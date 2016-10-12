# Topic      : USC CSCI 544 Applied NLP Fall 16 - HW2
#             - Perceptron Classifier for Spam-Ham classification
# Author     : Thamme Gowda Narayanaswamy
# Student ID : 2074-6694-39
# Email      : tnarayan@usc.edu
# Date       : Oct 12, 2016
import sys
import os
from perceptron import StdPerceptron
from perceptron import ENCODING
from perceptron import scan_data

def main(data_dir, model_path, out_path):
    print("Reading data from %s\nReading model from %s\n" \
        "Storing output to %s" % (data_dir, model_path, out_path))
    model = StdPerceptron.load_from_path(model_path)
    data = scan_data(data_dir)
    with open(out_path, 'w', 1, encoding=ENCODING) as outf:
        for label, path in data:
            vect = model.vectorize(path)
            pred = model.predict(vect)
            label = "spam" if pred > 0 else "ham"
            outf.write("%s %s\n" % (label, path))

if __name__ == '__main__':
    data_dir = sys.argv[1]
    out_path = sys.argv[2]
    model_path = 'per_model.txt'
    if not os.path.exists(model_path):
        print('Model doesnt exists at %s.' % model_path)
        sys.exit(3)
    main(data_dir, model_path, out_path)
