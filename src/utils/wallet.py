from src.utils.market_rules import MarketRules
from src.utils.my_warning import my_warning

class Wallet:
    def __init__(self, initial_nb_eur, initial_nb_xbt=0.0):
        self.my_nb_eur = initial_nb_eur # money that I invest
        self.my_nb_xbt = initial_nb_xbt # my amount of bitcoins
        self.market_rules = MarketRules()

    # This function is called when the predictor
    def buy_xbt(self, nb_eur_ttc, conversion_rate):
        nb_xbt = self.market_rules.how_much_xbt_do_i_really_get_for(nb_eur_ttc, conversion_rate)
        if nb_eur_ttc > self.my_nb_eur:
            my_warning("Not enough money.")
            return False
        elif nb_xbt < self.market_rules.minimum_xbt_to_trade:
            my_warning("Impossible to buy less than the minimum amount of XBT.")
            return False
        else:
            self.my_nb_eur -= nb_eur_ttc
            self.my_nb_xbt += nb_xbt
            return True

    # This function is only called when there is a gain, else we wait.
    def sell_xbt(self, amount_of_xbt, conversion_rate):
        #if amount_of_xbt < self.market_rules.minimum_xbt_to_trade:
        #    my_warning("Impossible to sell less than the minimum amount of XBT.")
        #    return 0.0
        #else:
        self.my_nb_xbt -= amount_of_xbt
        nb_eur = self.market_rules.how_much_eur_do_i_really_get_when_i_sell(amount_of_xbt, conversion_rate)
        self.my_nb_eur += nb_eur
        return nb_eur

    def how_much_do_i_possess_now(self, conversion_rate:float):
        return self.my_nb_eur + self.market_rules.how_much_eur_do_i_really_get_when_i_sell(self.my_nb_xbt, conversion_rate)

    @staticmethod
    def strf(x):
        return '%.2E' % x
        #return str(round(x * 100) / 100)

    def _repr_(self, conversion_rate):
        return (  self.strf(self.my_nb_eur) + " + "
                + self.strf(self.market_rules.how_much_eur_do_i_really_get_when_i_sell(self.my_nb_xbt, conversion_rate)) + " = "
                + self.strf(self.how_much_do_i_possess_now(conversion_rate)))