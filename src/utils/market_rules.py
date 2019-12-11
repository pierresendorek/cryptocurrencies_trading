from src.utils.my_warning import my_warning


class MarketRules:
    """
    Rules of the market.
    The methods here have no impact on my wallet.
    """

    def __init__(self):
        # TODO : find the actual values (should be smaller)
        # the following fees are valid for $0 - $50,000 transactions :
        self.taker_fees_proportion_buy = 0.26 / 100
        self.taker_fees_proportion_sell = 0.26 / 100
        self.minimum_xbt_to_trade = 0.002

    def get_minimal_amount_of_eur(self, conversion_rate_1xbt_to_eur):
        return self.minimum_xbt_to_trade * conversion_rate_1xbt_to_eur / (1 - self.taker_fees_proportion_buy)

    def how_much_xbt_after_tax_for(self, amount_of_eur, conversion_rate_1xbt_to_eur):
        fee = amount_of_eur * self.taker_fees_proportion_buy
        amount_of_eur_to_convert = amount_of_eur - fee
        conversion_rate_1eur_to_xbt = 1.0 / conversion_rate_1xbt_to_eur
        amount_of_xbt = amount_of_eur_to_convert * conversion_rate_1eur_to_xbt
        if amount_of_xbt < self.minimum_xbt_to_trade:
            my_warning("Impossible to buy less than the minimum amount of XBT.")
            return 0.0
        else:
            return amount_of_xbt

    def how_much_eur_after_tax_for(self, amount_of_xbt, conversion_rate_1xbt_to_eur):
        amount_of_eur = amount_of_xbt * conversion_rate_1xbt_to_eur
        fee = amount_of_eur * self.taker_fees_proportion_sell
        return amount_of_eur - fee

    def what_would_be_the_gain_if_i_sold(self, amount_of_xbt, conversion_rate, given_that_i_invested_nb_eur):
        gain = self.how_much_eur_after_tax_for(amount_of_xbt, conversion_rate) - given_that_i_invested_nb_eur
        return gain




if __name__ == "__main__":

    market_rules = MarketRules()
    nb_eur = market_rules.get_minimal_amount_of_eur(conversion_rate_1xbt_to_eur=7000)
    market_rules.how_much_xbt_after_tax_for(nb_eur, 7000)
