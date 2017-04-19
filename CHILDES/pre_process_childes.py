import os
import numpy as np
from CHILDES.ModifiedCHILDESCorpusReader import ModifiedCHILDESCorpusReader

file_dir = os.path.dirname(os.path.realpath(__file__))

########################################################################################################################

# helper functions


def remove_special_chars(utterance):

    special_chars = {'&', '!', '&', '"', '#', '$', '%', "'", '(', ')', '*', '+', ",", '-', '.', '/', ':', ';', '<',
                     '=', '>', '?', '@', '[', ']', '^', '_', '`', '{', '|', '}', '~', '\\'}

    utterance = [t for t in utterance if t not in special_chars]

    return utterance


def bootstrap_mlu(utterances, nr_samples=1000):
    """bootstrap MLU for utterances in transcript"""

    u_lengths = [len(u) for u in utterances]
    sample_size = len(u_lengths)

    sample_mlus = []
    for i in range(nr_samples):
        sample = np.random.choice(u_lengths, size=sample_size, replace=True)
        mlu = np.mean(sample)
        sample_mlus.append(mlu)

    bootstrap = np.mean(sample_mlus)

    return bootstrap


child_ids = dict()

def get_unique_child_id(participant_dict, corpus_name):
    """ Get unique ID (speaker name + corpus name) the target child in the transcript """

    child_name = participant_dict['CHI']['name']

    # sometimes the child's name is not given -- in that case, use corpus name instead
    # (this might underestimate the number of children, but  better to under- than overestimate)
    if type(child_name) != str:
        child_name = corpus_name

    child_key = child_name + corpus_name

    if child_key in child_ids:
        child_id = child_ids[child_key]
    elif len(child_ids) == 0:
        child_id = 0
        child_ids[child_key] = child_id
    else:
        child_id = max(set(child_ids.values())) + 1
        child_ids[child_key] = child_id

    return child_id


adult_ids = dict()

def get_unique_adult_ids(participant_dict, corpus_name):
    """ Get unique IDs (speaker name + corpus name)  for each adult speaker in the transcript """

    participant_keys = [i for i in participant_dict.keys() if i != 'CHI']
    ret = []
    for key in participant_keys:

        adult_name = participant_dict[key]['name']

        # sometimes the adult's name is not given -- in that case, use corpus name instead
        # (this might underestimate the number of adults, but  better to under- than overestimate)
        if type(adult_name) != str:
           adult_name = corpus_name

        adult_key = adult_name + corpus_name

        if adult_key in adult_ids:
            adult_id = adult_ids[adult_key]
        elif len(adult_ids) == 0:
            adult_id = 0
            adult_ids[adult_key] = adult_id
        else:
            adult_id = max(set(adult_ids.values())) + 1
            adult_ids[adult_key] = adult_id

        ret.append(adult_id)

    return ret


def get_child_adult_speakers(participant_dict):

    adult_speakers = set()
    child_speakers = set()

    for part in participant_dict:

        if participant_dict[part]['role'] != 'Target_Child':
            adult_speakers.add(participant_dict[part]['id'])
        else:
            child_speakers.add(participant_dict[part]['id'])

    return adult_speakers, child_speakers

########################################################################################################################


def process_CHILDES_corpus(corpus_path, MLU):
    """
    :param corpus_path: path to corpus .XML files
    :param speakers: adult speaker IDs whose utterances are to be considered (ignore all other adult speakers)
    """
    child_transcripts = []      # child-produced utterances (lists of utterances, which are themselves lists of words)
    adult_transcripts = []      # adult-produced utterances

    # additional data, by transcript
    ages = []                   # child ages
    MLUs = []                   # child MLUs
    corpus_names = []           # corpus names
    child_names = []            # name of child addressed
    adult_names = []            # names of adult speakers

    word_counter = 0
    corpus_reader = ModifiedCHILDESCorpusReader(corpus_path, u'.*.xml')

    # for each file in the corpus directory
    for fn in corpus_reader.fileids():

        participant_dict = corpus_reader.participants(fn)[0]
        adult_speakers, child_speakers = get_child_adult_speakers(participant_dict)
        adult_utterances = corpus_reader.sents(fn, adult_speakers, stem=False, relation=False, strip_space=True, replace=True)
        child_utterances = corpus_reader.sents(fn, child_speakers, stem=False, relation=False, strip_space=True, replace=True)

        age = corpus_reader.age(fn, month=True)[0]

        # getting unique child and adult IDs because the names are sometimes the same across different corpora
        # (e.g. the target  child is usually referred to as 'CHI')
        child_id = get_unique_child_id(participant_dict, corpus_path)
        adult_ids = get_unique_adult_ids(participant_dict, corpus_path)

        child_names.append(child_id)
        adult_names.append(adult_ids)

        transcript_adult = []
        transcript_child = []

        for utt in adult_utterances:
            utt = remove_special_chars(utt)
            utt = [w.lower() for w in utt]
            transcript_adult.append(utt)
            word_counter += len(utt)

        for utt in child_utterances:
            utt = remove_special_chars(utt)
            utt = [w.lower() for w in utt]
            transcript_child.append(utt)

        if MLU:
            if len(child_utterances) == 0:
                 continue

            mlu = bootstrap_mlu(transcript_child)
            MLUs.append(mlu)

        adult_transcripts.append(transcript_adult)
        child_transcripts.append(transcript_child)

        ages.append(age)
        corpus_names.append(corpus_path)

    print('Processed CHILDES corpus %s (%s adult tokens).' % (corpus_path, word_counter))
    return adult_transcripts, child_transcripts, ages, MLUs, corpus_names, child_names, adult_names


def process_childes_corpora(corpora, corpora_dir, MLU=False):
    """
    :param corpora: list of corpus names to be considered (names of directories in ./CHILDES/corpora/BE or .../NA)
    :param path to directory with corpora
    :return: a dictionary mapping keys to several lists:
        - 'adult_transcripts': contains lists of adult-produced utterances
        (each corresponding to a transcript from one of the corpora)
        - 'child_transcripts': contains lists of child-produced utterances
        - 'corpus_names': for each transcript, contains the name of its corpus
        - 'childe_ages': for each transcript, contains the age of the target child in months
        - 'child_MLU': for each transcript, contains the bootstrapped MLU of the target child
        - 'child_names': for each transcript, contains the name of the target child
        - 'adult_names': for each transcript, contains the names of the adults speakers
    """
    ret = {'child_transcripts': [],
           'adult_transcripts': [],
           'corpus_names': [],
           'child_ages': [],
           'child_MLU': [],
           'child_names': [],
           'adult_names': []}

    for corpus in corpora:
        corpus_path = '/'.join([file_dir, corpora_dir, corpus])
        adult_transcripts, child_transcripts, ages, MLUs, corpus_names, child_names, \
        adult_names = process_CHILDES_corpus(corpus_path, MLU)

        ret['adult_transcripts'] += adult_transcripts
        ret['child_transcripts'] += child_transcripts
        ret['child_ages'] += ages
        ret['child_MLU'] += MLUs
        ret['corpus_names'] += corpus_names
        ret['child_names'] += child_names
        ret['adult_names'] += adult_names

    print('Done processing corpus/corpora: %s' % corpora)
    print('Nr transcripts: %s' % len(ret['adult_transcripts']))
    print('Nr of different children: %s' % len(set(ret['child_names'])))

    return ret