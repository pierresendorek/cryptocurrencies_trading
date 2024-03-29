from typing import Iterator, Dict
import pandas as pd

class TransformDictToPandasRow:
    def __call__(self, iterator:Iterator[Dict]):
        for d in iterator:
            yield self.transform(d)

    def transform(self, d:Dict):
        return pd.Series(data=[*d.values()], index=d.keys())


if __name__ == "__main__":
    print(TransformDictToPandasRow().transform({"a":1, "b":2}))
