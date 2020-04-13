from src.pipelines.pipeline_elements.pipeline_element import PipelineElement
import pandas as pd

class Filter(PipelineElement):
    def __init__(self, boolean_function):
        PipelineElement.__init__(self)
        self.func = boolean_function

    def __call__(self, iterator:pd.Series):
        for x in iterator:
            if self.func(x):
                yield x

    def transform_dataframe(self, df:pd.DataFrame):
        return df[df.apply(self.func, axis=1)].copy()
