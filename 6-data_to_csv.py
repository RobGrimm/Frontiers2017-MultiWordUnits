import os
import csv
from DependentVariables.load_dependent_variables import get_reaction_times, get_AoFP
from pre_processed_corpora.load_freq_dict import load_freq_dict
from ChunkBasedLearner.load_mwus import load_mwus, load_random_baseline

file_dir = os.path.dirname(os.path.realpath(__file__))


def get_number_mwus_per_word(mwu_counter):

    ret = dict()
    for mwu, freq in mwu_counter.items():
        if len(mwu) == 1:
            continue
        for w in mwu:
            if w not in ret:
                ret[w] = 0
            ret[w] += 1
    return ret


def get_nr_of_mwus_per_target_word(target_words, mwu_type):

    # nr of different MWUs (types) per target word, in CDS and ADS
    ret = {'ADS': [], 'CDS': []}

    for corpus in ['CDS', 'ADS']:

        if mwu_type == 'CBL':
            mwu_counter = load_mwus(corpus)
        elif mwu_type == 'random_baseline':
            mwu_counter = load_random_baseline(corpus)
        else:
            raise Exception('mwu_type must be one of: CBL, random_baseline')

        nr_mwus_per_word = get_number_mwus_per_word(mwu_counter)
        ret[corpus] = [nr_mwus_per_word[w] if w in nr_mwus_per_word else 0 for w in target_words]

    return ret


def get_frequency_per_target_word(target_words):

    ads_freqs = load_freq_dict('ADS')
    cds_freqs = load_freq_dict('CDS')

    # frequency count of each target word -- for ADS and CDS corpus
    freq_per_words = {'ADS': [ads_freqs[w] for w in target_words], 'CDS': [cds_freqs[w] for w in target_words]}

    return freq_per_words


########################################################################################################################

# get target words

# only use words that (a) appear in both corpora and (b) for which we have both and AoFP estimate and a RT value
# a) get words that appear in both corpora
ads_freqs = load_freq_dict('ADS')
cds_freqs = load_freq_dict('CDS')
in_both_corpora = set(ads_freqs.keys()) & set(cds_freqs.keys())

# b) get words for which we have both RT and AoFP
AoFP_dict = get_AoFP()
RTs_dict = get_reaction_times()
with_RT_and_AoFP = set(AoFP_dict.keys()) & set(RTs_dict.keys())

# target words are all words that appear in both corpora and for which we have RT + AoFP
target_words = in_both_corpora & with_RT_and_AoFP

########################################################################################################################

# get dependent variables
freq_per_word = get_frequency_per_target_word(target_words)

nr_MWUs = get_nr_of_mwus_per_target_word(target_words, 'CBL')
nr_baseline = get_nr_of_mwus_per_target_word(target_words, 'random_baseline')

AoFP = [AoFP_dict[w] for w in target_words]
RTs = [RTs_dict[w] for w in target_words]

########################################################################################################################

# write results to CSV
with open(os.path.join(file_dir, 'results.csv'), 'w') as f:

    writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    measures = ['word', 'AoFP', 'RTs', 'CDS_freq', 'CDS_MWUs', 'CDS_random', 'ADS_freq', 'ADS_MWUs', 'ADS_random']
    writer.writerow(measures)

    for row in zip(*[target_words, AoFP, RTs, freq_per_word['CDS'], nr_MWUs['CDS'],
                     nr_baseline['CDS'], freq_per_word['ADS'], nr_MWUs['ADS'], nr_baseline['ADS']]):
        writer.writerow(row)