from ChunkBasedLearner.load_mwus import load_mwus, load_random_baseline


def print_mwus(corpus_name, begin_rank, end_rank, mwu_type):

    if mwu_type == 'CBL':
        mwu_counter = load_mwus(corpus_name)
    elif mwu_type == 'random_baseline':
        mwu_counter = load_random_baseline(corpus_name)
    else:
        raise Exception('mwu_type must be one of: CBL, random_baseline')

    print('############################################')
    print(corpus_name)
    print('############################################')
    print()

    # sort MWUs from most to least frequent
    sorted_mwus = sorted(list(mwu_counter.items()), key=lambda x: x[1], reverse=True)

    rank = 0
    idx = 0
    prev_freq = 99999999999999
    for mwu, freq in sorted_mwus:

        if freq < prev_freq:
            rank += 1
        prev_freq = freq

        idx += 1

        if begin_rank <= idx <= end_rank:
            print(' '.join(mwu), freq, rank, idx)

    print('total nr of rank: %s' % idx)


if __name__ == '__main__':
    # this prints MWUs from frequency rank 'begin_rank' to frequency rank 'end_rank'
    print_mwus(corpus_name='ADS', begin_rank=1, end_rank=100, mwu_type='CBL')




