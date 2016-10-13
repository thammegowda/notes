#!/usr/bin/env bash
TRAIN_DATA="../dataset/train"
TEST_DATA="../dataset/dev"
OUT_FILE="per_out.txt"
MODEL_FILE="per_model.txt"

# clean up
[ -f $MODEL_FILE ] && rm $MODEL_FILE
[ -f $OUT_FILE ] && rm $OUT_FILE

#Standard Perceptron
# Build the model
python3 per_learn.py $TRAIN_DATA
# Test
python3 per_classify.py $TEST_DATA $OUT_FILE
# Evaluate
python3 evalmodel.py $OUT_FILE

# Average Perceptron
# Build the model
python3 avg_per_learn.py $TRAIN_DATA
# Test
python3 per_classify.py $TEST_DATA $OUT_FILE
# Evaluate
python3 evalmodel.py $OUT_FILE


: <<'END_OF_COMMENT'
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
END_OF_COMMENT
