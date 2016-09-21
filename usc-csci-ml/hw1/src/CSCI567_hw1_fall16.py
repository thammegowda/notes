# Author     : ThammeGowda Narayanaswamy
# Email      : tnarayan@usc.edu
# Student ID : 2074669439
# Subject    : K Nearest Neighbor implementation for CSCI 567 Fall 16 Homework 1
# Date       : September 17, 2016
import nb_classify as nb
import knn_classify as knn
import sys

def main(train_path, test_path):
    print("Naive Bayes Classifier:")
    nb.main(train_path, test_path)
    print("\nK Nearest Neighbor Classifier")
    knn.main(train_path, test_path)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("((No args supplied; Using the default args))")
        train_path = "dataset/train.txt"
        test_path = "dataset/test.txt"
    else:
        train_path = sys.argv[1]
        train_path = sys.argv[2]
    main(train_path, test_path)
