from src.feature_engineering.datum_formatter import DatumFormatter
from src.load_dataframe.data_loader import DataLoader
from src.pipelines.pipeline_elements.dataset_stream import DatasetStream
from src.pipelines.pipeline_elements.iterate_over_iterable import IterateOverIterable
from src.pipelines.pipeline_elements.kraken_stream import KrakenStream
from src.pipelines.pipeline_elements.pipeline import Pipeline
from src.pipelines.pipeline_elements.transform_to_pandas_row import TransformToPandasRow

mock = True

if mock:
    print("Using stored files")
    data = DataLoader().load()
    df = data.get_uninterrupted_datasets()[0]
    data_source = DatasetStream(df).get_iterator()

else:
    print("Using Kraken stream")
    kraken_source = KrakenStream(verbose=False).get_stream_of_data()
    pipeline = Pipeline(steps=[DatumFormatter(),
                               IterateOverIterable(),
                               TransformToPandasRow()])
    data_source = pipeline(kraken_source)




for x in data_source:
    print(x)
