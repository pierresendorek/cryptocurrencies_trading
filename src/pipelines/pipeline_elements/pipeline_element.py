from typing import Iterator

import pandas as pd


class PipelineElement:
    def __call__(self, iterator:Iterator):
        raise NotImplementedError

    def transform_dataframe(self, df:pd.DataFrame):
        raise NotImplementedError