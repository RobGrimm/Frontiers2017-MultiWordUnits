import os
import pickle
from pre_processed_corpora.load_pre_processed_corpus import load_cds, load_ads
from ChunkBasedLearner.ChunkBasedLearner import ChunkBasedLearner


file_dir = os.path.dirname(os.path.realpath(__file__))


########################################################################################################################

# 1) process ADS corpus

utterances = load_ads()

# CBL
cbl = ChunkBasedLearner(random_btp=False)
mwu_counter = cbl.get_mwus(utterances)
with open(os.path.join(file_dir, 'ChunkBasedLearner', 'ADS.pickle'), 'wb') as f:
    pickle.dump(mwu_counter, f, protocol=pickle.HIGHEST_PROTOCOL)

# random baseline
baseline = ChunkBasedLearner(random_btp=True)
mwu_counter = baseline.get_mwus(utterances)
with open(os.path.join(file_dir, 'ChunkBasedLearner', 'ADS_baseline.pickle'), 'wb') as f:
    pickle.dump(mwu_counter, f, protocol=pickle.HIGHEST_PROTOCOL)

########################################################################################################################

# 2) process CDS corpus

utterances = load_cds()

# CBL
cbl = ChunkBasedLearner(random_btp=False)
mwu_counter = cbl.get_mwus(utterances)
with open(os.path.join(file_dir, 'ChunkBasedLearner', 'CDS.pickle'), 'wb') as f:
    pickle.dump(mwu_counter, f, protocol=pickle.HIGHEST_PROTOCOL)

# random baseline
baseline = ChunkBasedLearner(random_btp=True)
mwu_counter = baseline.get_mwus(utterances)
with open(os.path.join(file_dir, 'ChunkBasedLearner', 'CDS_baseline.pickle'), 'wb') as f:
    pickle.dump(mwu_counter, f, protocol=pickle.HIGHEST_PROTOCOL)