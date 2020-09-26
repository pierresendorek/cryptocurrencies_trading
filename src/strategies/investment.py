from src.utils.market_rules import MarketRules
from src.utils.wallet import Wallet


class Investment:
    def __init__(self, spent_nb_eur, bought_nb_xbt):
        self.spent_nb_eur = spent_nb_eur
        self.bought_nb_xbt = bought_nb_xbt

    def is_profitable(self, conversion_rate_sell, market_rules):
        nb_eur_sell = market_rules.how_much_eur_do_i_really_get_when_i_sell(self.bought_nb_xbt, conversion_rate_sell)
        if nb_eur_sell > self.spent_nb_eur:
            return True
        else:
            return False

    def profitability_ratio(self, conversion_rate_sell, market_rules):
        nb_eur_sell = market_rules.how_much_eur_do_i_really_get_when_i_sell(self.bought_nb_xbt, conversion_rate_sell)
        return nb_eur_sell / self.spent_nb_eur

    def __repr__(self):
        return str(self.__dict__)