#!/usr/bin/env bash

# clean up
[ -f nbmodel.txt ] && rm nbmodel.txt
[ -f nboutput.txt ] && rm nboutput.txt

TRAIN_DATA="../dataset/train"
TEST_DATA="../dataset/dev"

# Build the model
python3 nblearn.py $TRAIN_DATA

# Test the model
python3 nbclassify.py $TEST_DATA

# Evaluate the model
python3 evalmodel.py nboutput.txt

#: <<'END_OF_COMMENT'
# Get ten percent of random data
# 5% percent from spam and 5% from ham
n=`find $TRAIN_DATA -type f | wc -l`
count=`expr $n / 20`
TMP_DIR="./tmp"

[ -d $TMP_DIR ] && rm -r $TMP_DIR
mkdir -p $TMP_DIR
find $TRAIN_DATA -type f | grep spam | shuf | shuf | head -$count | while read i; do cp $i $TMP_DIR; done
find $TRAIN_DATA -type f | grep ham | shuf | shuf | head -$count | while read i; do cp $i $TMP_DIR; done

# Build the model
python3 nblearn.py $TMP_DIR

# Test the model
python3 nbclassify.py $TEST_DATA

# Evaluate the model
python3 evalmodel.py nboutput.txt
#END_OF_COMMENT
