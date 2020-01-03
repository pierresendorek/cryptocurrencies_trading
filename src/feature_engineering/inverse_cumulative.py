
from sortedcontainers import SortedDict
from copy import deepcopy



def how_much_equivalent_euro_can_i_get(xbt2eur_histogram:SortedDict, total_amount_xbt):
    xbt2eur_histogram = deepcopy(xbt2eur_histogram)
    cumulated_amount_xbt = 0.0
    cumulated_amount_eur = 0.0

    while cumulated_amount_xbt < total_amount_xbt:
        if len(xbt2eur_histogram) == 0:
            return float("NaN")
        conversion_rate, amount_xbt = xbt2eur_histogram.peekitem(0)
        needed_amount_xbt = total_amount_xbt - cumulated_amount_xbt
        if amount_xbt < needed_amount_xbt:
            cumulated_amount_xbt += amount_xbt
            cumulated_amount_eur += amount_xbt * conversion_rate
            xbt2eur_histogram.popitem(0)
        else: # amount_xbt >= needed_amount_xbt
            #cumulated_amount_xbt += needed_amount_xbt
            cumulated_amount_eur += needed_amount_xbt * conversion_rate
            break
    return cumulated_amount_eur




def how_much_equivalent_xbt_can_i_get(xbt2eur_histogram:SortedDict, total_amount_eur):
    xbt2eur_histogram = deepcopy(xbt2eur_histogram)
    cumulated_amount_xbt = 0.0
    cumulated_amount_eur = 0.0

    while cumulated_amount_eur < total_amount_eur:
        if len(xbt2eur_histogram) == 0:
            return float("NaN")
        conversion_rate, amount_xbt = xbt2eur_histogram.peekitem(-1)
        needed_amount_eur = total_amount_eur - cumulated_amount_eur
        amount_eur = amount_xbt * conversion_rate
        if amount_eur < needed_amount_eur:
            cumulated_amount_xbt += amount_xbt
            cumulated_amount_eur += amount_eur
            xbt2eur_histogram.popitem(-1)
        else: # amount_eur < needed_amount_eur
            cumulated_amount_xbt += needed_amount_eur / conversion_rate
            #cumulated_amount_eur += needed_amount_eur
            break
    return cumulated_amount_xbt



# usage example
if __name__ == "__main__":
    d = SortedDict({8000: 0.001, 8100: 0.01, 8200:0.01})

    print(d)
    print(how_much_equivalent_xbt_can_i_get(d, 160))






