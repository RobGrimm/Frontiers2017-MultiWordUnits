import os
import json
from CHILDES.pre_process_childes import process_childes_corpora

file_dir = os.path.dirname(os.path.realpath(__file__))

########################################################################################################################

british_corpora = ['Belfast', 'Fletcher', 'Manchester', 'Thomas', 'Tommerdahl', 'Wells', 'Forrester', 'Lara']

# process CHILDES .xml files
corpus_dict = process_childes_corpora(corpora=british_corpora, corpora_dir='corpora/BE/', MLU=True)

# write processed corpus data to disk for future usage
json.dump(corpus_dict, open('/'.join([file_dir, 'pre_processed_corpora', 'CDS.json']), 'w'))