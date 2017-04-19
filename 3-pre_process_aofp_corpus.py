import os
import json
from CHILDES.pre_process_childes import process_childes_corpora

file_dir = os.path.dirname(os.path.realpath(__file__))

########################################################################################################################

# NOTE: there are 47 folders but only 44 corpora ('Demetras1' and 'Demetras2' are one corpus,
# as are 'VanKleeck' and 'VanKleeck 2', as well as 'Feldman' and 'Feldman 2')
american_corpora = ['Bates', 'Bernstein', 'Bliss', 'Bloom70', 'Bloom73', 'Bohannon', 'Braunwald', 'Brent', 'Brown',
                    'Carterette', 'Clark', 'Cornell', 'Demetras1', 'Demetras2', 'ErvinTripp', 'Evans', 'Feldman',
                    'Feldman 2', 'Garvey', 'Gathercole',  'Gleason', 'HSLLD', 'Hall', 'Higginson', 'Kuczaj',
                    'MacWhinney', 'McCune', 'McMillan',  'Morisset', 'Nelson', 'NewEngland', 'Peters', 'Post',
                    'Providence', 'Rollins', 'Sachs', 'Snow', 'Soderstrom', 'Sprott', 'Suppes', 'Tardif', 'Valian',
                    'VanHouten', 'VanKleeck', 'VanKleeck 2', 'Warren', 'Weist']


# process CHILDES .xml files
corpus_dict = process_childes_corpora(corpora=american_corpora, corpora_dir='corpora/NA/', MLU=True)

# write processed corpus data to disk for future usage
json.dump(corpus_dict, open('/'.join([file_dir, 'pre_processed_corpora', 'AoFP.json']), 'w'))