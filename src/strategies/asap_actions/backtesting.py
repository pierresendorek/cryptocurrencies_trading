from src.feature_engineering.datum_formatter import DatumFormatter
from src.load_dataframe.data_loader import DataLoader
from src.pipelines.feature_engineering_pipeline import FeatureEngineeringPipeline
from src.pipelines.pipeline_elements.dataset_stream import DatasetStream
from src.pipelines.pipeline_elements.iterate_over_iterable import IterateOverIterable
from src.pipelines.pipeline_elements.kraken_stream import KrakenStream
from src.pipelines.pipeline_elements.ordinary_pipeline import OrdinaryPipeline
from src.pipelines.pipeline_elements.transform_dict_to_pandas_row import TransformDictToPandasRow
from src.strategies.asap_actions.context import Context
from src.strategies.asap_actions.features import Features, FeaturesComputer
from src.strategies.asap_actions.params import Params
from src.strategies.asap_actions.phases import Initialization

mock = True

feature_engineering_pipeline = FeatureEngineeringPipeline()

if mock:
    print("Using stored files")
    data = DataLoader().load()
    df = data.get_uninterrupted_datasets()[4]
    df = feature_engineering_pipeline.transform_dataframe(df)
    data_source = DatasetStream(df).get_row_iterator()



else:
    print("Using Kraken stream")
    kraken_source = KrakenStream(verbose=False).get_stream_of_data_as_iterator()
    pipeline = OrdinaryPipeline(steps=[DatumFormatter(),
                                       IterateOverIterable(),
                                       TransformDictToPandasRow()])
    data_source = pipeline(kraken_source)
    data_source = feature_engineering_pipeline(data_source)


import numpy as np
params = Params(target_interest=0.005, nb_eur_to_invest=20.0, initialization_time=60*60*24)
context = Context()

phase = Initialization(params, context)

features_computer = FeaturesComputer(smoothing_time=60*60*24, slope_time=30)

c_list = []
t_list = []

import matplotlib.pyplot as plt
from time import sleep

for x in data_source:
    #print(x.to_dict())
    f = features_computer(x['conversion_rate'], x['time_as_float'])
    print(context.wallet.how_much_do_i_possess_now(x['conversion_rate']))
    c_list.append(x['conversion_rate'])
    t_list.append(x['time_as_float'])
    #print(f)
    phase = phase(f)



plt.plot(t_list, c_list)
#plt.show()

buy_list = [(x[1].conversion_rate, x[1].time) for x in context.info_collector if x[0] == "Buy"]
sell_list = [(x[1].conversion_rate, x[1].time) for x in context.info_collector if x[0] == "Sell"]


s = list(zip(*sell_list))
if len(s) > 0:
    plt.scatter(s[1], s[0], c='r', s=150)

b = list(zip(*buy_list))
if len(b) > 0:
    plt.scatter(b[1], b[0], c='g', s=150)

print(context.info_collector)

plt.show()

