import os
import json


def get_file_path():
    return os.path.dirname(os.path.realpath(__file__))


def load_childes_corpus_dict(corpus_name):
    assert corpus_name in ['CDS', 'AoFP']
    dir = '/'.join([get_file_path(), '%s.json' % corpus_name])
    corpus_dict = json.load(open(dir, 'r'))
    return corpus_dict


def load_cds():

    # CDS corpus is stored in dictionary format and needs to be re-factored before we can return it
    corpus_dict = load_childes_corpus_dict('CDS')

    # 1) order transcripts by child MLU
    zipped = zip(corpus_dict['child_MLU'], corpus_dict['adult_transcripts'])
    ordered = sorted(zipped)
    transcripts = [t for mlu, t in ordered]

    # 2) convert list of transcripts into flat list of utterances
    utterances = []
    for u in transcripts:
        utterances.extend(u)

    return utterances


def load_ads():
    dir = '/'.join([get_file_path(), 'ADS.json'])
    # ADS corpus is already stored in correct format
    utterances = json.load(open(dir, 'r'))
    return utterances


def load_aofp_corpus():

    # AoFP corpus is stored in dictionary format and needs to be re-factored before we can return it
    corpus_dict = load_childes_corpus_dict('AoFP')

    # 1) order transcripts by child MLU
    zipped = zip(corpus_dict['child_MLU'], corpus_dict['child_transcripts'])
    ordered = sorted(zipped)
    transcripts = [t for mlu, t in ordered]

    # 2) convert list of transcripts into flat list of utterances
    utterances = []
    for u in transcripts:
        utterances.extend(u)

    return utterances
