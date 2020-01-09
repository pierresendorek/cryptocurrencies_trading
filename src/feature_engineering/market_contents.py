import numpy as np
from sortedcontainers import SortedDict
from pprint import pprint

class MarketContents:
    def __init__(self, nb_items_to_keep=10**5):
        self.current_sells = SortedDict()
        self.current_buys = SortedDict()
        self.nb_items_to_keep = nb_items_to_keep

    def update_contents(self, row):
        if row["sell_buy"] == "s":
            self._add_to_distibution(self.current_sells, row["conversion_rate"], row["amount"])
        if row["sell_buy"] == "b":
            self._add_to_distibution(self.current_buys, row["conversion_rate"], row["amount"])
        self._make_deals()
        self.random_forget_if_too_much_elements()

    def random_forget_if_too_much_elements(self):
        for collection in [self.current_buys, self.current_sells]:
            if len(collection) > self.nb_items_to_keep:
                nb_elements_to_remove = len(collection) - self.nb_items_to_keep
                idx_of_elements_to_remove = sorted(np.random.choice(len(collection), size=nb_elements_to_remove, replace=False), reverse=True)
                for index in idx_of_elements_to_remove:
                    collection.popitem(index)

    def _add_to_distibution(self, d: dict, key, increment):
        value = d.get(key, 0)
        d[key] = value + increment

    def _make_deals(self):
        all_deals_made = False
        while not all_deals_made:
            if len(self.current_buys) == 0 or len(self.current_sells) == 0:
                all_deals_made = True
            else:
                conversion_rate_buy, amount_buy = self._take_highest_buy()
                conversion_rate_sell, amount_sell = self._take_lowest_sell()
                if conversion_rate_sell > conversion_rate_buy:
                    all_deals_made = True
                else: # conversion_rate_sell <= conversion_rate_buy:
                    if amount_buy < amount_sell:
                        left_to_sell = amount_sell - amount_buy
                        self._pop_highest_buy()
                        self.current_sells[conversion_rate_sell] = left_to_sell
                    elif amount_buy > amount_sell:
                        left_to_buy = amount_buy - amount_sell
                        self._pop_lowest_sell()
                        self.current_buys[conversion_rate_buy] = left_to_buy
                    else: # amount_buy == amount_sell
                        self._pop_lowest_sell()
                        self._pop_highest_buy()

    def _pop_highest_buy(self):
        self.current_buys.popitem(-1)

    def _pop_lowest_sell(self):
        self.current_sells.popitem(0)

    def _take_lowest_sell(self):
        return self.current_sells.peekitem(0)

    def _take_highest_buy(self):
        return self.current_buys.peekitem(-1)