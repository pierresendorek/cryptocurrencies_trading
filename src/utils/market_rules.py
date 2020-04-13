from src.utils.my_warning import my_warning


class MarketRules:
    """
    Rules of the market.
    The methods here have no impact on my wallet.
    """

    def __init__(self):
        # TODO : get the real values from the server
        # the following fees are valid for $0 - $50,000 transactions :
        self.taker_fees_proportion_buy = 0.26 / 100
        self.taker_fees_proportion_sell = 0.26 / 100
        self.minimum_xbt_to_trade = 0.002

    def gain_factor(self, conversion_rate_buy, conversion_rate_sell):
        buy_price = self.how_much_eur_costs_buying(1.0, conversion_rate_buy)
        sell_price = self.how_much_eur_do_i_really_get_when_i_sell(1.0, conversion_rate_sell)
        return (sell_price - buy_price) / buy_price

    def how_much_eur_costs_buying(self, nb_xbt, conversion_rate_buy):
        nb_eur = conversion_rate_buy * nb_xbt
        fee = nb_eur * self.taker_fees_proportion_buy
        return nb_eur + fee

    def how_much_eur_do_i_really_get_when_i_sell(self, nb_xbt, conversion_rate_sell):
        nb_eur = nb_xbt * conversion_rate_sell
        fee = nb_eur * self.taker_fees_proportion_sell
        return nb_eur - fee








if __name__ == "__main__":

    market_rules = MarketRules()
    nb_eur = market_rules.get_minimal_amount_of_eur(conversion_rate_1xbt_to_eur=7000)
