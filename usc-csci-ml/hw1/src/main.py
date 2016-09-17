# Author     : ThammeGowda Narayanaswamy
# Email      : tnarayan@usc.edu
# Student ID : 2074669439
# Subject    : K Nearest Neighbor implementation for CSCI 577 Fall 16 Homework 1
# Date       : September 17, 2016
import nb_classify as nb
import knn_classify as knn
import sys

def main(train_path, test_path):
    print("Naive Bayes Classifier")
    nb.main(train_path, test_path)
    print("\nK Nearest Neighbor Classifier")
    knn.main(train_path, test_path)

if __name__ == '__main__':
    if len(sys.argv) != 3:
      print("Error: Invalid args")
      print("Usage: %s <data/train.txt> <data/test.txt>" % sys.argv[0])
      sys.exit(1)
    main(sys.argv[1], sys.argv[2])
