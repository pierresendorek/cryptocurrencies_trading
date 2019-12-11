from src.utils.market_rules import MarketRules
from src.utils.my_warning import warning

class Wallet:
    def __init__(self, initial_nb_eur, spare_proportion=0.5):
        self.my_nb_eur_to_use = initial_nb_eur # money that I invest
        self.my_nb_eur_spared = 0.0 # money that I keep for me forever
        self.my_nb_xbt = 0.0 # my amount of bitcoins

        self.spare_proportion = spare_proportion
        self.market_rules = MarketRules()

    def buy_xbt(self, amount_of_eur, conversion_rate):
        if amount_of_eur > self.my_nb_eur_to_use:
            warning("Not enough money.")
            return 0.0
        else:
            nb_xbt = self.market_rules.how_much_xbt_after_tax_for(amount_of_eur, conversion_rate)
            if nb_xbt < self.market_rules.minimum_xbt_to_trade:
                warning("Impossible to buy less than the minimum amount of XBT.")
                return 0.0
            else:
                fee = amount_of_eur * self.market_rules.taker_fees_proportion_buy
                # amount_of_eur_to_convert = amount_of_eur - fee
                self.my_nb_eur_to_use -= amount_of_eur
                # got_nb_xbt = amount_of_eur_to_convert * conversion_rate
                # self.my_nb_xbt += nb_xbt
                return got_nb_xbt

    # This function is only called when there is a gain, else we wait.
    def sell_xbt(self, amount_of_xbt, conversion_rate, invested_nb_eur):
        if amount_of_xbt < self.market_rules.minimum_xbt_to_trade:
            warning("Impossible to sell less than the minimum amount of XBT.")
            return 0.0
        else:
            nb_eur = self.market_rules.how_much_eur_after_tax_for(amount_of_xbt, conversion_rate)
            gain = nb_eur - invested_nb_eur
            self.my_nb_eur_to_use += gain * (1 - self.spare_proportion)
            self.my_nb_eur_spared += gain * self.spare_proportion
            return nb_eur

    def how_much_do_i_possess_now(self, conversion_rate):
        return self.my_nb_eur_spared + self.my_nb_eur_to_use + self.market_rules.how_much_eur_after_tax_for(self.my_nb_xbt, conversion_rate)

    @staticmethod
    def strf(x):
        return str(round(x * 100) / 100)

    def _repr_(self, conversion_rate):
        return (self.strf(self.my_nb_eur_spared) + " + "
                + self.strf(self.my_nb_eur_to_use) + " + "
                + self.strf(self.market_rules.how_much_eur_after_tax_for(self.my_nb_xbt, conversion_rate)) + " = "
                + self.strf(self.how_much_do_i_possess_now(conversion_rate)))