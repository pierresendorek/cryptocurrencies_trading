from src.feature_engineering.smoothing import RollingMaxCausal, RollingMinCausal
from src.strategies.investment import Investment
from src.utils.wallet import Wallet
from typing import List


class CautiousOpportunists:

    def __init__(self, patience_to_consider_is_at_bottom, patience_to_consider_is_at_top, percentage_of_increase_tolerance, initial_nb_eur):
        self.wallet = Wallet(initial_nb_eur=initial_nb_eur)
        self.rolling_max = RollingMaxCausal(win_len=patience_to_consider_is_at_top)
        self.rolling_min = RollingMinCausal(win_len=patience_to_consider_is_at_bottom)
        self.percentage_of_increase_tolerance = percentage_of_increase_tolerance

        self.prev_max_conversion_rate = - float('inf')
        self.prev_min_conversion_rate = float('inf')

        self.has_reached_a_maximum_once = False
        self.going_uphill = True
        self.time_to_sell_asap = False

        self.investments: List[Investment] = []

        self.prev_conversion_rate_buy = 0.0
        self.prev_conversion_rate_sell = float('inf')

        self.nb_eur_to_invest_at_next_step = 0.0



    def __call__(self, row):
        time = row['time_as_float']
        conversion_rate = row['conversion_rate']

        # buying
        if self.nb_eur_to_invest_at_next_step > 0.0:
            pessimistic_conversion_rate = max(conversion_rate, self.prev_conversion_rate_buy)
            self.invest(self.nb_eur_to_invest_at_next_step, pessimistic_conversion_rate)
            self.nb_eur_to_invest_at_next_step = 0.0

        if self.time_to_sell_asap:
            pessimistic_conversion_rate = min(conversion_rate, self.prev_conversion_rate_sell)
            self.sell_all_profitable_investments(pessimistic_conversion_rate)
            self.time_to_sell_asap = False

        max_conversion_rate = self.rolling_max(time, conversion_rate)
        min_conversion_rate = self.rolling_min(time, conversion_rate)

        if (min_conversion_rate > self.prev_min_conversion_rate) and self.has_reached_a_maximum_once and not self.going_uphill:  # just started going uphill
            if conversion_rate / self.prev_min_conversion_rate < self.percentage_of_increase_tolerance:
                self.enqueue_action_invest(nb_eur_ttc=20.0, conversion_rate=conversion_rate)
            self.going_uphill = True

        if (max_conversion_rate < self.prev_max_conversion_rate) and self.going_uphill:  # started going downhill
            self.enqueue_action_sell_all_profitable_investments(conversion_rate)
            self.going_uphill = False
            self.has_reached_a_maximum_once = True

        self.prev_max_conversion_rate = max_conversion_rate
        self.prev_min_conversion_rate = min_conversion_rate
        self.prev_conversion_rate_sell = conversion_rate
        self.prev_conversion_rate_buy = conversion_rate



    def enqueue_action_invest(self, nb_eur_ttc, conversion_rate):
        self.nb_eur_to_invest_at_next_step = nb_eur_ttc
        self.prev_conversion_rate_buy = conversion_rate

    def enqueue_action_sell_all_profitable_investments(self, conversion_rate):
        self.prev_conversion_rate_sell = conversion_rate
        self.time_to_sell_asap = True


    def invest(self, nb_eur_ttc, conversion_rate):
        nb_xbt = self.wallet.market_rules.how_much_xbt_do_i_really_get_for(nb_eur_ttc, conversion_rate=conversion_rate)
        buy_success = self.wallet.buy_xbt(nb_eur_ttc=nb_eur_ttc, conversion_rate=conversion_rate)
        if buy_success:
            self.investments.append(Investment(nb_eur_ttc, nb_xbt))


    def sell_all_profitable_investments(self, conversion_rate):
        remaining_investments = []
        for investment in self.investments:
            if investment.is_profitable(conversion_rate, self.wallet.market_rules):
                self.wallet.sell_xbt(investment.bought_nb_xbt, conversion_rate)
            else:
                remaining_investments.append(investment)
        self.investments = remaining_investments




if __name__ == '__main__':
    import matplotlib.pyplot as plt
    import numpy as np

    h = CautiousOpportunists(patience_to_consider_is_at_bottom=10,
                             patience_to_consider_is_at_top=6)

    v_list = []
    nb_xbt_list = []
    nb_eur_list = []
    equiv_nb_eur_list = []
    m = []

    for i in range(500):
        v =  2 + np.sin(2 * np.pi * i / 100) + np.random.rand() / 2 # + 100 * np.cos(2*np.pi * i / 250)
        v_list.append(v)
        h({'time_as_float':float(i), 'conversion_rate':v})
        nb_xbt_list.append(h.wallet.my_nb_xbt)
        nb_eur_list.append(h.wallet.my_nb_eur)
        equiv_nb_eur_list.append(h.wallet.how_much_do_i_possess_now(v))

    #print(nb_eur_list)
    plt.plot(v_list, label='conversion_rate')
    plt.plot(nb_eur_list, label='my_nb_eur')
    plt.plot(nb_xbt_list, label='my_nb_xbt')
    plt.plot(np.array(equiv_nb_eur_list), label='total_equiv_amount_eur')

    plt.legend()
    plt.show()


