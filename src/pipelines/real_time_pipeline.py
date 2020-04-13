from src.feature_engineering.datum_formatter import DatumFormatter
from src.load_dataframe.data_loader import DataLoader
from src.pipelines.feature_engineering_pipeline import FeatureEngineeringPipeline
from src.pipelines.pipeline_elements.dataset_stream import DatasetStream
from src.pipelines.pipeline_elements.iterate_over_iterable import IterateOverIterable
from src.pipelines.pipeline_elements.kraken_stream import KrakenStream
from src.pipelines.pipeline_elements.pipeline import Pipeline
from src.pipelines.pipeline_elements.transform_dict_to_pandas_row import TransformDictToPandasRow

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
    pipeline = Pipeline(steps=[DatumFormatter(),
                               IterateOverIterable(),
                               TransformDictToPandasRow(),
                               feature_engineering_pipeline])
    data_source = pipeline(kraken_source)


from time import sleep
for x in data_source:
    print(x.to_dict())
    sleep(1.0)

