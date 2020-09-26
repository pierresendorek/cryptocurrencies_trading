from src.strategies.investment import Investment
from src.utils.market_rules import MarketRules
from src.utils.wallet import Wallet
from typing import List

class Context:
    def __init__(self):
        self.wallet = Wallet(initial_nb_eur=100.0, initial_nb_xbt=0.0)
        self.investments:List[Investment] = []
        self.market_rules = MarketRules()

    def has_profitable_investment(self, conversion_rate:float) -> bool:
        for investment in self.investments:
            if investment.is_profitable(conversion_rate, self.market_rules):
                return True
        return False

    def enqueue_action_buy(self, conversion_rate):
        self.wallet.buy_xbt(nb_eur_ttc=20, conversion_rate=conversion_rate)

    def enqueue_action_sell(self, conversion_rate):
        for investment in self.investments:
            self.wallet.sell_xbt(amount_of_xbt=self.wallet.my_nb_xbt, conversion_rate=conversion_rate)