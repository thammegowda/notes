import os
import sys
import math
import pickle
import logging as log
log.basicConfig(level=log.DEBUG)

ENCODING = 'latin-1'

class NaiveBayesModel(object):

    def __init__(self, paths):
        self.labels = sorted(paths.keys())
        self.label_ct = {}
        self.token_ct = {}
        self.totaltoken_ct = {}
        for label, pths in paths.items():
            self.label_ct[label] = len(pths)
            self.token_ct[label] = self.token_stats(pths)
            self.totaltoken_ct[label] = sum(self.token_ct[label].values())
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

    def predict(self, doc):
        #log.debug("Predict ::%s" % doc)
        tokens = self.tokenize(doc)
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
                if not tok in self.token_ct[label]:
                    print("Ignoring: %s - %s" %(label, tok))
                    continue
                P_tok_given_label =  float(self.token_ct[label][tok]) / self.totaltoken_ct[label]
                P_doc_given_label_log += math.log(P_tok_given_label)

            res = math.log(P_label) + P_doc_given_label_log
            preds[label] = res
        return preds

    def tokenize(self, text):
        return text.split()

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
