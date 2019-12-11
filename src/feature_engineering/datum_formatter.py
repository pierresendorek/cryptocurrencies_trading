import datetime

class DatumFormatter:
    def __init__(self):
        pass

    def get_currency_pair(self, datum):
        return datum[3]

    def get_datum_operation_type(self, datum):
        return datum[2]

    def get_id(self, datum):
        return datum[0]

    def _get_conversion_rate(self, transaction):
        return float(transaction[0])

    def _get_amount(self, transaction):
        return float(transaction[1])

    def _get_time(self, transaction):
        t = float(transaction[2])
        return datetime.datetime.fromtimestamp(t)

    def _get_sell_buy(self, transaction):
        return transaction[3]

    def _get_l_or_m(self, transaction):
        return transaction[4]

    def extract(self, datum):
        id, transaction_list, transaction_type, currency_pair = datum[0:4]

        functions_to_apply = [self._get_time,
                              self._get_conversion_rate,
                              self._get_amount,
                              self._get_sell_buy,
                              self._get_l_or_m]

        formatted_transaction_list = [self._format_transaction(currency_pair,
                                                               functions_to_apply,
                                                               id,
                                                               transaction,
                                                               transaction_type) for transaction in transaction_list]

        return formatted_transaction_list



    def _format_transaction(self, currency_pair, functions_to_apply, id, transaction, transaction_type):
        d = {"id": id,
             "currency_pair": currency_pair,
             "transaction_type": transaction_type}
        for function in functions_to_apply:
            d[function.__name__[5:]] = function(transaction)
        return d


if __name__ == "__main__":
    from pprint import pprint

    #datum = [14, [['8954.50000', '0.00903986', '1565942559.843509', 's', 'l', '']], 'trade', 'XBT/EUR']
    datum = [92, [['183.16000', '7.31548350', '1565944311.649186', 's', 'l', ''],
                  ['183.10000', '10.00000000', '1565944311.653790', 's', 'l', ''],
                  ['183.00000', '11.20000000', '1565944311.656357', 's', 'l', ''],
                  ['182.98000', '2.99999975', '1565944311.658677', 's', 'l', ''],
                  ['182.98000', '0.00000025', '1565944311.661254', 's', 'l', ''],
                  ['182.97000', '28.66700000', '1565944311.692677', 's', 'l', '']], 'trade', 'ETH/USD']


    pprint(DatumFormatter().extract(datum))
