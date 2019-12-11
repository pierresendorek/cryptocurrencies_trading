import unittest

from src.utils.market_rules import MarketRules


class TestMarketRules(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.market_rules = MarketRules()

    def test_minimal_investment_for_xbt_enough(self):
        # given __init__
        conversion_rate = 7000

        # when
        nb_eur = self.market_rules.get_minimal_amount_of_eur(conversion_rate_1xbt_to_eur=conversion_rate)
        nb_xbt = self.market_rules.how_much_xbt_after_tax_for(nb_eur, conversion_rate)

        # then
        self.assertAlmostEqual(nb_xbt, self.market_rules.minimum_xbt_to_trade)