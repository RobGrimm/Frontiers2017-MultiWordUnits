import os
import pickle


file_dir = os.path.dirname(os.path.realpath(__file__))


def load_mwus(corpus_name):
    mwus = pickle.load(open(os.path.join(file_dir, 'MWUs', '%s.pickle' % corpus_name), 'rb'))
    return mwus


def load_random_baseline(corpus_name):
    baseline = pickle.load(open(os.path.join(file_dir, 'MWUs', '%s_baseline.pickle' % corpus_name), 'rb'))
    return baseline