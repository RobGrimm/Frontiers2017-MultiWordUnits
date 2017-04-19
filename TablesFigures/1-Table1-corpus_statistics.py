import os
import numpy as np
import scipy.stats
from pre_processed_corpora.load_pre_processed_corpus import load_cds, load_ads, load_aofp_corpus, load_childes_corpus_dict


file_dir = os.path.dirname(os.path.realpath(__file__))


def get_corpus_statistics():

    ads = load_ads()
    cds = load_cds()
    aofp = load_aofp_corpus()

    ret = dict()

    for corpus_name, corpus in [('CDS', cds), ('ADS', ads), ('AoFP', aofp)]:

        all_tokens = []
        all_types = set()
        utt_lengths = []

        for u in corpus:

            if len(u) == 0:
                continue

            utt_lengths.append(len(u))
            all_tokens += u
            all_types.update(u)

        ret[corpus_name] = (all_tokens, all_types, utt_lengths)

    return ret


def print_corpus_info():

    corpus_statistics_dict = get_corpus_statistics()

    for corpus_name, stats in corpus_statistics_dict.items():

        all_tokens, all_types, utt_lengths = stats

        print(corpus_name)
        print('nr tokens: %s' % len(all_tokens))
        print('nr types: %s' % len(all_types))
        print('nr sentences: %s' % len(utt_lengths))
        print('mean utterance length: %s (std: %s)' % (np.median(utt_lengths), scipy.stats.iqr(utt_lengths)))
        print()


def print_nr_speakers_in_childes_corpus(corpus_name):

    cds_dict = load_childes_corpus_dict(corpus_name)

    all_adults = []
    for adults in cds_dict['adult_names']:
        all_adults += adults

    all_children = []
    for children in cds_dict['child_names']:
        all_children += [children]

    print('nr of adult speakers in %s: %s' % (corpus_name, len(set(all_adults))))
    print('nr of child speakers in %s: %s' % (corpus_name, len(set(all_children))))


if __name__ == '__main__':

    print_corpus_info()
    print_nr_speakers_in_childes_corpus('CDS')
    print_nr_speakers_in_childes_corpus('AoFP')
