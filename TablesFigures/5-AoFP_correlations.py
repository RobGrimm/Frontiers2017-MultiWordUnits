from scipy.stats import spearmanr
from DependentVariables.load_dependent_variables import get_aoa_morrison, get_AoFP, get_reaction_times


def correlate_aoa_aofp_rts():
    """ correlate AoA values from Morrison et al. (1997), RTs from the English Lexicon Project, and AoFP """

    morrison = get_aoa_morrison()
    induced = get_AoFP()

    # AoFP VS morrison
    words = set(morrison).intersection(induced)
    aoa1 = [morrison[w] for w in words]
    aoa2 = [induced[w] for w in words]
    rho, p_value = spearmanr(aoa1, aoa2)
    print('Nr of words shared between Morrison and AoFP %s' % len(words))
    print("Spearman's rho: %s  (p: %s)" % (rho, p_value))
    print()

    # morrison vs reaction times
    rts_by_word = get_reaction_times()
    words = set(morrison).intersection(rts_by_word)
    aoa1 = [morrison[w] for w in words]
    aoa2 = [rts_by_word[w] for w in words]
    rho, p_value = spearmanr(aoa1, aoa2)
    print('Nr of words shared between Morrison and RTs: %s' % len(words))
    print("Spearman's rho: %s  (p: %s)" % (rho, p_value))
    print()

    # AoFP vs reaction times
    words = set(induced).intersection(rts_by_word)
    aoa1 = [induced[w] for w in words]
    aoa2 = [rts_by_word[w] for w in words]
    rho, p_value = spearmanr(aoa1, aoa2)
    print('Nr of words shared between AoFP and RTs: %s' % len(words))
    print("Spearman's rho: %s  (p: %s)" % (rho, p_value))
    print()


if __name__ == '__main__':
    correlate_aoa_aofp_rts()
