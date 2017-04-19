import os
import json

file_dir = os.path.dirname(os.path.realpath(__file__))

########################################################################################################################

# load corpus data
corpus_dict = json.load(open('/'.join(['pre_processed_corpora', 'AoFP.json']), 'r'))

# order transcripts in corpus by child MLU (from smallest to largest MLU)
zipped = zip(corpus_dict['child_MLU'], corpus_dict['child_transcripts'])
ordered = sorted(zipped)

aofp_dict = dict()

for mlu, transcript in ordered:
    for utt in transcript:
        for word in utt:
            if word not in aofp_dict:
                aofp_dict[word] = mlu

# store AoFP dictionary on disk
json.dump(aofp_dict, open('/'.join([file_dir, 'DependentVariables', 'data', 'AoFP.json']), 'w'))

print('Got AoFP for %s words' % len(aofp_dict))