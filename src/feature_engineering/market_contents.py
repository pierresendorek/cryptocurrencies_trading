import numpy as np
from sortedcontainers import SortedDict
from pprint import pprint

from src.feature_engineering.datum_formatter import DatumFormatter
from src.pipelines.pipeline_elements.filter import Filter
from src.pipelines.pipeline_elements.iterate_over_iterable import IterateOverIterable
from src.pipelines.pipeline_elements.kraken_stream import KrakenStream
from src.pipelines.pipeline_elements.pipeline import Pipeline
from src.pipelines.pipeline_elements.lambda_function import Lambda
from src.pipelines.pipeline_elements.transform_dict_to_pandas_row import TransformDictToPandasRow
from src.utils.data_structures.cell import Cell
from src.utils.data_structures.heap_deque import HeapDeque


class MarketContents:
    def __init__(self, nb_items_to_keep=10**6):
        print("initializing MarketContents...")
        self.current_sells = HeapDeque(max_nb_items=nb_items_to_keep, sort_order='ascending')
        self.current_buys = HeapDeque(max_nb_items=nb_items_to_keep, sort_order='descending')
        print("done")

    def update_contents(self, row):
        if row["sell_buy"] == "s":
            self.current_sells.append(Cell(conversion_rate=row["conversion_rate"], amount=row["amount"]))
        if row["sell_buy"] == "b":
            self.current_buys.append(Cell(conversion_rate=row["conversion_rate"], amount=row["amount"]))
        self._make_deals()


    def _make_deals(self):
        all_deals_made = False
        while not all_deals_made:
            if len(self.current_buys) == 0 or len(self.current_sells) == 0:
                all_deals_made = True
            else:
                highest_buy = self._take_highest_buy()
                lowest_sell = self._take_lowest_sell()

                if lowest_sell.conversion_rate > highest_buy.conversion_rate:
                    all_deals_made = True
                else: # conversion_rate_sell <= conversion_rate_buy:
                    if highest_buy.amount < lowest_sell.amount:
                        left_to_sell = lowest_sell.amount - highest_buy.amount
                        lowest_sell.amount = left_to_sell
                    elif highest_buy.amount > lowest_sell.amount:
                        left_to_buy = highest_buy.amount - lowest_sell.amount
                        highest_buy.amount = left_to_buy
                    else: # amount_buy == amount_sell
                        self._pop_lowest_sell()
                        self._pop_highest_buy()

    def _pop_highest_buy(self):
        cell = self.current_buys.pop_root()
        return cell.conversion_rate, cell.amount

    def _pop_lowest_sell(self):
        cell = self.current_sells.pop_root()
        return cell.conversion_rate, cell.amount

    def _take_lowest_sell(self) -> Cell:
        return self.current_sells.heap.get_root()

    def _take_highest_buy(self) -> Cell:
        return self.current_buys.heap.get_root()



if __name__ == "__main__":
    market_contents = MarketContents()

    kraken_source = KrakenStream(verbose=False).get_stream_of_data_as_iterator()
    pipeline = Pipeline(steps=[DatumFormatter(),
                               IterateOverIterable(),
                               Filter(lambda d: d['currency_pair'] == 'XBT/EUR'),
                               TransformDictToPandasRow()])
    data_source = pipeline(kraken_source)

    for i, row in enumerate(data_source):
        market_contents.update_contents(row)
        if (i % 100) == 0:
            print(row.to_dict())
            print("-!o" * 40)
            print("Sells")
            print("-"*80)
            market_contents.current_sells.heap.print_subtree()
            print("Buys")
            print("-" * 80)
            market_contents.current_sells.heap.print_subtree()
            print("-" * 80)

