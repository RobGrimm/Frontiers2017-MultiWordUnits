from collections import defaultdict
from nltk.util import ngrams
import random


class RandomChunkBasedLearner(object):

    def __init__(self):

        self.co_occurrences = defaultdict(lambda: defaultdict(int))

        # if word_b in follows[word_a], then word_a follows word_b in some chunk that is already stored in memory
        self.follows = defaultdict(set)

        self.chunk_counter = defaultdict(int)



    def get_MWUs(self, token_sents):

        n_sent = 0

        for tokens in token_sents:

            n_sent += 1

            for idx, token in enumerate(tokens):

                token = tokens[idx]

                if idx == 0:
                    chunk = [token]
                    continue

                left_token = tokens[idx - 1]

                BTP = random.uniform(0, 1)
                mean_BTP = 0.5

                if BTP > mean_BTP or token in self.follows[left_token]:
                    chunk.append(token)
                else:
                    self.store_chunk(chunk)
                    chunk = [token]

                if idx == len(tokens) - 1 and len(chunk) > 0:
                    self.store_chunk(chunk)

            if n_sent % 10000 == 0:
                print(n_sent / len(token_sents))

        return self.chunk_counter


    def store_chunk(self, chunk):

        chunk = tuple(chunk)

        if len(chunk) > 1:

            self.chunk_counter[chunk] += 1
            self.update_follows(chunk)


    def update_follows(self, chunk):

        for a, b in ngrams(chunk, 2):
            self.follows[a].add(b)