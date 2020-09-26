from src.feature_engineering.datum_formatter import DatumFormatter
from src.load_dataframe.data_loader import DataLoader
from src.pipelines.feature_engineering_pipeline import FeatureEngineeringPipeline
from src.pipelines.pipeline_elements.dataset_stream import DatasetStream
from src.pipelines.pipeline_elements.iterate_over_iterable import IterateOverIterable
from src.pipelines.pipeline_elements.kraken_stream import KrakenStream
from src.pipelines.pipeline_elements.ordinary_pipeline import OrdinaryPipeline
from src.pipelines.pipeline_elements.transform_dict_to_pandas_row import TransformDictToPandasRow
from src.strategies.extremal_actions.context import Context
from src.strategies.extremal_actions.features_computer import FeaturesComputer
from src.strategies.extremal_actions.finite_state_transducers import Initialization, Params

mock = True

feature_engineering_pipeline = FeatureEngineeringPipeline()

if mock:
    print("Using stored files")
    data = DataLoader().load()
    df = data.get_uninterrupted_datasets()[0]
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



params = Params(time_to_wait_before_initialized=10, mock_trades=True, abnormality_threshold=-3.0)
features_computer = FeaturesComputer(t_linear_prediction_long_term=60 * 12, t_linear_prediction_short_term=60*5)
context = Context()
phase = Initialization(params=params, context=context)

from time import sleep
for x in data_source:
    #print(x.to_dict())
    f = features_computer.compute(x['conversion_rate'], x['time_as_float'])
    #print(f)
    phase = phase(f)


