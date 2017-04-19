import os
import json
from collections import defaultdict

file_dir = os.path.dirname(os.path.realpath(__file__))


def get_AoFP():
    """ load and return AoFP dictionary """
    return json.load(open('/'.join([file_dir, 'data', 'AoFP.json']), 'r'))


def get_aoa_morrison():
    """
    Return a dictionary mapping words to their age of acquisition value from Morrison et al. (1997).
    AoA data were kindly provided by Catriona Morrison.
    """
    aoa_by_word = dict()
    with open('/'.join([file_dir, 'data', 'morrison.txt']), 'r') as file_:

        for line in file_:
            word, aoa_lr, aoa = line.split()[:3]
            word = word.strip()
            aoa = aoa.strip()

            # don't have AoA for two words
            # ingore these words
            if aoa == '-':
                continue

            aoa_by_word[word] = float(aoa)

    return aoa_by_word


def get_reaction_times():
    """
    Return a dictionary mapping words to their mean reaction times from the English Lexicon Project.
    """
    rts_by_word = defaultdict(list)

    with open('/'.join([file_dir, 'data', 'EnglishLexiconProjectFull.csv']), 'r') as file_:

        for idx, line in enumerate(file_):

            if idx == 0:
                continue

            line = [i.strip() for i in line.split(',')]

            if line == ['']:
                continue

            word, length, freq, log_freq, pos_tag1, mean_rt, mean_acc = [i.strip('"') for i in line]

            if mean_rt == 'NULL':
                continue

            mean_rt = float(mean_rt)
            word = word.lower()

            rts_by_word[word] = mean_rt

    return rts_by_word