from src.strategies.investment import Investment
from src.utils.market_rules import MarketRules
from src.utils.wallet import Wallet
from typing import List



class Context:
    def __init__(self):
        self.wallet:Wallet = Wallet(initial_nb_eur=100.0, initial_nb_xbt=0.0)
        self.investments:List[Investment] = []
        self.info_collector = []
        self.last_conversion_rate_sell = None



