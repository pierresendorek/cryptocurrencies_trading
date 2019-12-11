from src.utils.market_rules import MarketRules
from src.utils.wallet import Wallet
from datetime import timedelta, datetime
from time import time

class TargetProfitability:
    def __init__(self):
        self.list_of_invested_nb_eur_and_expected_xbt = []

    def update(self, nb_eur, expected_nb_xbt):
        self.list_of_invested_nb_eur_and_expected_xbt.append((nb_eur, expected_nb_xbt))



class HippoGloutonStrategy:
    def __init__(self,
                 time_horizon,
                 predictor_sell_price_will_continue_to_raise,
                 predictor_of_opportunities_to_invest,
                 initial_nb_eur=249.85,
                 proportion_to_invest=0.05):

        # accounts
        self.wallet = Wallet(initial_nb_eur=initial_nb_eur)

        # parameters
        self.proportion_to_invest = proportion_to_invest
        self.threshold_minimum_probability_of_raising_value = 0.9
        self.threshold_minimum_probaility_of_good_opportunity = 0.9
        self.disbelief_threshold = 0.1
        self.time_horizon = time_horizon

        # state
        self.target_profitability = TargetProfitability()
        self.last_date_of_buying_xbt = None

        # utils
        self.market_rules = MarketRules()
        self.predictor_sell_price_will_continue_to_raise = predictor_sell_price_will_continue_to_raise
        self.predictor_of_opportunities_to_invest = predictor_of_opportunities_to_invest


    def process(self, row):
        probability_good_opportunity_to_invest = self.predictor_of_opportunities_to_invest(row)

        if probability_good_opportunity_to_invest > self.threshold_minimum_probaility_of_good_opportunity:
            self.action_when_prediction_to_invest_is_favourable(row["conversion_rate"])
        else:
            self.action_when_prediction_to_invest_is_not_favourable(row["conversion_rate"])

    def action_when_prediction_to_invest_is_favourable(self, buy_conversion_rate):
        money_to_invest = self.compute_how_much_money_to_invest(buy_conversion_rate)
        current_time = datetime.fromtimestamp(time())
        if (self.last_date_of_buying_xbt is not None) and (current_time > self.last_date_of_buying_xbt + self.time_horizon):
            nb_xbt = self.wallet.buy_xbt(money_to_invest, buy_conversion_rate)
            self.target_profitability.update(nb_eur=money_to_invest, expected_nb_xbt=nb_xbt)
            self.last_date_of_buying_xbt = current_time

    def action_when_prediction_to_invest_is_not_favourable(self, sell_conversion_rate):
        if self.probability_sell_price_will_continue_to_raise() > self.threshold_minimum_probability_of_raising_value:
            pass # wait
        else: # will not (so surely) continue to raise
            total_invested_nb_eur_to_sell, total_xbt_to_sell = self.select_profitable_xbt(sell_conversion_rate)

            self.wallet.sell_xbt(amount_of_xbt=total_xbt_to_sell,
                                 conversion_rate=sell_conversion_rate,
                                 invested_nb_eur=total_invested_nb_eur_to_sell)

    def select_profitable_xbt(self, sell_conversion_rate):
        list_of_not_yet_profitable_invested_eur = []
        total_xbt_to_sell = 0.0
        total_invested_nb_eur_to_sell = 0.0
        for invested_nb_eur, nb_xbt in self.target_profitability.list_of_invested_nb_eur_and_expected_xbt:
            gain_if_i_sold_xbt = self.market_rules.what_would_be_the_gain_if_i_sold(nb_xbt, sell_conversion_rate,
                                                                                    given_that_i_invested_nb_eur=invested_nb_eur)
            if gain_if_i_sold_xbt > 0:
                total_xbt_to_sell += nb_xbt
                total_invested_nb_eur_to_sell += invested_nb_eur
            else:
                list_of_not_yet_profitable_invested_eur.append((invested_nb_eur, nb_xbt))
        self.target_profitability.list_of_invested_nb_eur_and_expected_xbt = list_of_not_yet_profitable_invested_eur
        return total_invested_nb_eur_to_sell, total_xbt_to_sell

    # TODO : predictor
    def probability_sell_price_will_continue_to_raise(self):
        return 0.5

    def compute_how_much_money_to_invest(self, buy_conversion_rate):
        minimal_nb_eur = self.market_rules.get_minimal_amount_of_eur(conversion_rate_1xbt_to_eur=buy_conversion_rate)
        amount_to_prevent_rounding_errors = 0.01
        equivalent_nb_eur_to_sell_after_investment = max([self.wallet.my_nb_eur_to_use * self.proportion_to_invest, minimal_nb_eur + amount_to_prevent_rounding_errors])
        nb_eur_to_invest = equivalent_nb_eur_to_sell_after_investment / ((1 - self.market_rules.taker_fees_proportion_buy) * (1 - self.market_rules.taker_fees_proportion_sell))
        return nb_eur_to_invest

