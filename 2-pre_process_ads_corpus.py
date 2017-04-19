import os
import json
from BNC.pre_process_bnc import process_bnc_files, get_spoken_demographic_fileids

file_dir = os.path.dirname(os.path.realpath(__file__))

########################################################################################################################

# process BNC .xml files that make up the 'Spoken Demographic BNC'
ads_corpus = process_bnc_files(fileids=get_spoken_demographic_fileids())

# write processed corpus data to disk for future usage
json.dump(ads_corpus, open('/'.join([file_dir, 'pre_processed_corpora', 'ADS.json']), 'w'))