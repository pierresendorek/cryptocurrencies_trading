from src.strategies.asap_actions.context import Context
from src.strategies.asap_actions.features import Features, FeaturesComputer
from src.strategies.asap_actions.params import Params
from src.strategies.investment import Investment
import numpy as np



class Initialization:
    def __init__(self, params:Params, context:Context):
        self.params = params
        self.context = context
        self.initialization_time = None

    def __call__(self, f:Features):
        if self.initialization_time is None:
            self.initialization_time = f.time
        if f.time - self.initialization_time > self.params.initialization_time:
            return WaitForOpportunityToBuy(self.params, self.context)
        else:
            return self



class WaitForOpportunityToBuy:
    def __init__(self, params, context:Context):
        self.params = params
        self.context = context

    def __call__(self, f:Features):

        stddev_of_log = np.sqrt(f.smoothed_sigma2_of_log)
        avg_log_conversion_rate = f.smoothed_log_conversion_rate

        #period_of_high_variability = stddev_of_log / avg_log_conversion_rate > 0.5 * np.log(1 + self.params.target_interest)
        conversion_rate_abnormally_low = np.log(f.conversion_rate) < avg_log_conversion_rate #- 0.1 * stddev_of_log

        if self.context.last_conversion_rate_sell is None:
            if conversion_rate_abnormally_low:
                return Buy(self.params, self.context)(f)
            else:
                return self

        if self.context.wallet.market_rules.gain_factor(f.conversion_rate, self.context.last_conversion_rate_sell) > self.params.target_interest \
                and f.slope_of_log_conversion_rate >= 0 and f.prev_slope_of_log_conversion_rate < 0:
            return Buy(self.params, self.context)(f)
        else:
            return self



class Buy:
    def __init__(self, params:Params, context:Context):
        self.params = params
        self.context = context

    def __call__(self, f:Features):
        nb_xbt_bought = self.context.wallet.market_rules.how_much_xbt_do_i_really_get_for(self.params.nb_eur_to_invest, f.conversion_rate)
        if self.context.wallet.buy_xbt(self.params.nb_eur_to_invest, f.conversion_rate):
            self.context.investments.append(Investment(self.params.nb_eur_to_invest, nb_xbt_bought))
            self.context.info_collector.append(("Buy", f))

        return WaitForOpportunityToSell(self.params, self.context)


class WaitForOpportunityToSell:
    def __init__(self, params, context):

        self.params = params
        self.context = context

    def __call__(self, f:Features):
        for investment in self.context.investments:
            if investment.profitability_ratio(conversion_rate_sell=f.conversion_rate, market_rules=self.context.wallet.market_rules) > 1 + self.params.target_interest \
                    and f.prev_slope_of_log_conversion_rate > 0.0 and f.slope_of_log_conversion_rate < 0.0:
                return Sell(self.params, self.context)(f, investment)
        return self


class Sell:
    def __init__(self, params, context):
        self.params = params
        self.context = context

    def __call__(self, f:Features, investment:Investment):
        self.context.wallet.sell_xbt(amount_of_xbt=investment.bought_nb_xbt, conversion_rate=f.conversion_rate)
        self.context.investments = []
        self.context.info_collector.append(("Sell", f))
        self.context.last_conversion_rate_sell = f.conversion_rate
        return WaitForOpportunityToBuy(self.params, self.context)(f)





if __name__ == "__main__":
    import numpy as np
    params = Params(target_interest=0.03, nb_eur_to_invest=20.0, initialization_time=10)
    context = Context()

    phase = Initialization(params, context)

    features_computer = FeaturesComputer(smoothing_time=20, slope_time=2)

    c_list = []
    c = 8000.0
    for it in range(100000):
        c = c * np.exp(np.random.randn() * 0.01)
        #c = 8000 + 1000 * np.sin(np.pi * it / 16)
        f = features_computer(conversion_rate=c, time=1.0 * it)
        phase = phase(f)
        print(context.wallet.how_much_do_i_possess_now(c))
        c_list.append(c)



    import matplotlib.pyplot as plt

    plt.plot(c_list)
    #plt.show()

    buy_list = [(x[1].conversion_rate, x[1].time) for x in context.info_collector if x[0] == "Buy"]
    sell_list = [(x[1].conversion_rate, x[1].time) for x in context.info_collector if x[0] == "Sell"]

    b = list(zip(*buy_list))
    s = list(zip(*sell_list))
    plt.scatter(s[1], s[0], c='r')
    plt.scatter(b[1], b[0], c='b')

    print(context.info_collector)

    plt.show()





