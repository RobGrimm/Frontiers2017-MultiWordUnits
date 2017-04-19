import random
from collections import defaultdict
from nltk.util import ngrams


class ChunkBasedLearner(object):

    def __init__(self, random_btp=False):

        self.co_occur = defaultdict(lambda: defaultdict(int))   # self.co_occur[w][left_w] is the frequency with which
                                                                # 'left_w' has immediately preceded'w'
        self.freqs = defaultdict(int)       # word frequencies
        self.mwu_counter = dict()           # multi-word unit (MWU) frequencies
        self.follows = defaultdict(set)     # if word_b in follows[word_a], then word_b follows word_a
                                            # in some multi-word unit that is already stored in memory

        self.random_btp = random_btp        # if True, BTP will be randomly selected and compared against a mean BTP
                                            # of 0.5 (used as a baseline model)

    def get_mwus(self, utterances):

        n_utts = 0
        for u in utterances:
            n_utts += 1

            # iterate over utterances
            for idx, w in enumerate(u):
                w = u[idx]
                self.freqs[w] += 1

                # if 'w' is the first word in the utterance,
                # consider it as the first potential word in an MWU
                if idx == 0:
                    mwu = [w]
                    continue

                left_w = u[idx - 1]
                # update co-occurrence count
                self.co_occur[w][left_w] += 1

                # get backward transitional probability (BTP) of 'left_w' given 'w' and mean BTP for 'w'
                btp, mean_btp = self.get_btps(w, left_w)

                # add current word ('w') to MWU if:
                #   a) the BTP is larger than the mean BTP plus the reciprocal of the frequeqncy of 'w' OR
                #   b) 'w' immediately follows 'left_w' in one of MWUs already in memory
                if btp > mean_btp + 1 / self.freqs[w] or w in self.follows[left_w]:
                    mwu.append(w)
                # otherwise, store current MWU and create a new MWU with 'w' as its only member
                else:
                    self.store_mwu(mwu)
                    mwu = [w]

                # store MWU if we are done processing the current utterance and we have a non-empty MWU
                if idx == len(u) - 1 and len(mwu) > 0:
                    self.store_mwu(mwu)

            if n_utts % 10000 == 0:
                print(n_utts / len(utterances))

        return self.mwu_counter


    def get_btps(self, w, left_w):

        if self.random_btp:
            btp = random.uniform(0, 1)
            mean_btp = 0.5

        else:
            # frequency of 'w'
            freq = float(self.freqs[w])

            # BTP of 'left_w' given 'w': P(left_w | w)
            btp = self.co_occur[w][left_w] / freq

            # get mean co-occurrence count of 'w' across all words that have appeared to the left of 'w'
            all_co_occur = sum(self.co_occur[w].values())
            all_left_words = len(self.co_occur[w].keys())
            mean_co_occur = all_co_occur / all_left_words

            # mean BTP for 'w'
            mean_btp = mean_co_occur / self.freqs[w]

        return btp, mean_btp


    def store_mwu(self, mwu):

        mwu = tuple(mwu)

        if len(mwu) > 1:
            if mwu not in self.mwu_counter:
                self.mwu_counter[mwu] = 0

            self.mwu_counter[mwu] += 1
            self.update_follows(mwu)


    def update_follows(self, mwu):

        for word1, word2 in ngrams(mwu, 2):
            self.follows[word1].add(word2)