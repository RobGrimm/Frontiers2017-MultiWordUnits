import os
import csv
from pre_processed_corpora.load_pre_processed_corpus import load_childes_corpus_dict


file_dir = os.path.dirname(os.path.realpath(__file__))


def aofp_corpus_info_to_csv():

    corpus_dict = load_childes_corpus_dict('AoFP')
    child_transcripts = corpus_dict['child_transcripts']
    ages = corpus_dict['child_ages']
    child_names = corpus_dict['child_names']

    with open('/'.join([file_dir, 'AoFP_corpus_info.csv']), 'w') as f:

        writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        measures = ['transcript', 'nr_child_tokens', 'child_age', 'child_name']
        writer.writerow(measures)

        for id_, child_transcript, age, name in zip(range(len(child_transcripts)), child_transcripts, ages, child_names):

            n_child_tokens = sum([len(utt) for utt in child_transcript])
            row = [id_, n_child_tokens, age, name]
            writer.writerow(row)


if __name__ == '__main__':
    # save relevant information to CSV first using this function call
    # after that, use Figure1.R to plot the information from R
    aofp_corpus_info_to_csv()