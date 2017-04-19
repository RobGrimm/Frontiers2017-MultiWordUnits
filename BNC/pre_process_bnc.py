import os
import fnmatch
from nltk.corpus import BNCCorpusReader


def get_file_path():
    return os.path.dirname(os.path.realpath(__file__))


def get_bnc_path():
    return '/'.join([get_file_path(), 'corpus'])


def get_bnc_fileids():
    ids = []
    for root, dirnames, filenames in os.walk(get_bnc_path() + '/Texts/'):
      for filename in fnmatch.filter(filenames, '*.xml'):
        ids.append(os.path.join(root, filename))
    return ids


def get_spoken_demographic_fileids():
    """return paths to spoken demographic BNC files"""

    # get all BNC file paths
    all_bnc_ids = get_bnc_fileids()

    # get spoken demographic file IDs
    spoken_demog = []
    with open('/'.join([get_bnc_path(), 'spoken_demog.txt']), 'r') as f:
        for file_name in f:
            spoken_demog.append(file_name.strip())

    # retain only BNC file paths that contain a spoken demographic file ID
    ret = []
    for i in spoken_demog:
        for j in all_bnc_ids:
            if i in j:
                ret.append(j)
    return ret


def replace_clitics(token_sentence):
    """
    replaces clitics like "'m" or "n't" with their full orthographic forms (e.g. "'m" --> "am", "n't" --> "not")
    """
    s = ' '.join(token_sentence)
    s = ' ' + s + ' '

    # map clitics to their full forms
    clitic_dict = {"'m ": ' am ', "'re ": ' are ', "'s ": ' is ', "'ve ": ' have ', "n't ": ' not ',
                   "'ll": ' will ', "'d ": ' would ', 'not ': ' not ', 'gonna': ' going to '}

    # replace clitcs with full form
    for clitic, full_form in clitic_dict.items():
            s = s.replace(clitic, full_form)

    return s.split()


def remove_special_chars(sent):

    special_chars = {'&', '!', '&', '"', '#', '$', '%', "'", '(', ')', '*', '+', ",", '-', '.', '/', ':', ';', '<',
                     '=', '>', '?', '@', '[', ']', '^', '_', '`', '{', '|', '}', '~', '\\', '‘', '’'}

    sent = [w for w in sent if w not in special_chars]

    return sent


def process_bnc_files(fileids):

    bnc = BNCCorpusReader(fileids=fileids, root=get_bnc_path() + '/Texts/')
    utterances = bnc.sents()

    ret = []
    for u in utterances:

        try:
            u = remove_special_chars(u)
            u = replace_clitics(u)
            u = [str(w).lower() for w in u]     # remove POS tags and lower-case words

            if len(u) == 0:
                continue

            ret.append(u)

        except UnicodeEncodeError:
            continue

    return ret