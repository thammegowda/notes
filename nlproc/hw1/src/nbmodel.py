# Topic      : USC CSCI 544 Applied NLP Fall 16 - HW1
#             - Naive Bayes Classifier for Spam-Ham classification
# Author     : Thamme Gowda Narayanaswamy
# Student ID : 2074-6694-39
# Email      : tnarayan@usc.edu
# Date       : Sept 22, 2016
import os
import sys
import math
import pickle
import logging as log
log.basicConfig(level=log.DEBUG)

ENCODING = 'latin-1'
EN_STOPWORDS=set(["a", "an", "and", "are", "as", "at", "be", "but", "by", \
                "for", "if", "in", "into", "is", "it", \
                "no", "not", "of", "on", "or", "such", \
                "that", "the", "their", "then", "there", "these", \
                "they", "this", "to", "was", "will", "with"])
class NaiveBayesModel(object):
    __VERSION__ = 1

    def __init__(self, paths):
        self.__version__ = NaiveBayesModel.__VERSION__
        self.labels = sorted(paths.keys())
        self.label_ct = {}
        self.token_ct = {}
        self.totaltoken_ct = {}
        self.vocabulary = set()
        for label, pths in paths.items():
            self.label_ct[label] = len(pths)
            stats = self.token_stats(pths)
            self.token_ct[label] = stats
            self.totaltoken_ct[label] = sum(stats.values())
            self.vocabulary.update(stats.keys())
        self.label_pb = {}

        total_examples = sum(self.label_ct.values())
        if total_examples == 0:
            raise Exception('No records found')
        for label in self.labels:
            self.label_pb[label] = 1.0 * self.label_ct[label] / total_examples
            print("P(%s) = %f " % (label, self.label_pb[label]))
            print("Total Tokens(%s) = %d " % (label, self.totaltoken_ct[label]))

    def token_stats(self, paths):
        res = {}
        paths = filter(lambda p: os.path.exists(p), paths)
        for path in paths:
            with open(path, encoding=ENCODING) as f:
                for tok in self.tokenize(f.read()):
                    res[tok] = res.get(tok, 0) + 1
        return res

    def additive_smoothing_predict(self, tok, label, alpha=1):
        return float(self.token_ct[label].get(tok, 0) + alpha) / \
               (self.totaltoken_ct[label] + alpha * len(self.vocabulary))

    def predict(self, doc):
        #log.debug("Predict ::%s" % doc)
        tokens = self.tokenize(doc)
        # filter : ignore tokens that arent seen
        tokens = list(filter(lambda tok: tok in self.vocabulary, tokens))
        if not tokens:
            raise Exception("Completely New text: %s" % doc)
        preds = {}
        for label in self.labels:
            '''
               # Bayes rule
               P(label|doc) = P(label) * P (doc|label)
                               -------------------------
                                  P(doc)

               # the naive assumption of independence
               P (doc | label) = P (tok1|label) * P(tok2|label) * ..... * P(tok'n'|label)

               # ignore denominator
            '''
            P_label = self.label_pb[label]
            P_doc_given_label_log = 0
            for tok in tokens:
                try:
                    #P_tok_given_label =  float (self.token_ct[label][tok]) / self.totaltoken_ct[label]
                    P_tok_given_label = self.additive_smoothing_predict(tok, label, alpha=1)
                    P_doc_given_label_log += math.log(P_tok_given_label)
                except:
                    continue
            res = math.log(P_label) + P_doc_given_label_log
            preds[label] = res
        return preds

    def tokenize(self, text, unigrams=True, bigrams=True, stopwords=False):
        tokens = []
        unigrams = text.split()
        if stopwords:
            unigrams = list(filter(lambda x: x not in EN_STOPWORDS, unigrams))
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
            model = pickle.load(f)
            if model.__version__ != NaiveBayesModel.__VERSION__:
                log.warn("Model may not be compatible, class version %d," \
                    + " serialized model version:%d" %
                    (NaiveBayesModel.__VERSION__, model.__version__))
            else:
                log.info("Model version %d" % model.__version__)
            return model
