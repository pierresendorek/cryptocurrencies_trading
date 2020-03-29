import krakenex
import warnings

from conf import ConfigProject


class ApiCommunication:
    def __init__(self):
        self.k = krakenex.API()
        self.k.load_key(ConfigProject().kraken_keys_file)

    def get_balance(self):
        """
        Example of res =
        {'error': [],
         'result': {'ZEUR': '762.5055',
                    'XXBT': '0.0020000000',
                    'LINK': '0.0000000000'}}
        """

        res = self.k.query_private('Balance')
        if res['error'] != []:
            warnings.warn('error during get_balance ' + str(res['error']))
        return res['result']


    def buy_at_market_price(self, nb_xbt:float):
        assert isinstance(nb_xbt, float)
        self.k.query_private('AddOrder', {'pair': 'XXBTZEUR',
                                     'type': 'buy',
                                     'ordertype': 'market',
                                     'volume': nb_xbt})

    def sell_at_market_price(self, nb_xbt:float):
        assert isinstance(nb_xbt, float)
        self.k.query_private('AddOrder', {'pair': 'XXBTZEUR',
                                     'type': 'sell',
                                     'ordertype': 'market',
                                     'volume': nb_xbt})

    def buy_limit(self, nb_xbt, for_nb_eur):
        self.k.query_private('AddOrder', {'pair': 'XXBTZEUR',
                                          'type': 'buy',
                                          'ordertype': 'limit',
                                          'price': for_nb_eur,
                                          'volume': nb_xbt})

    def sell_limit(self, nb_xbt, for_nb_eur):
        self.k.query_private('AddOrder', {'pair': 'XXBTZEUR',
                                     'type': 'sell',
                                     'ordertype': 'limit',
                                     'price': for_nb_eur,
                                     'volume': nb_xbt})


