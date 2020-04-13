from src.load_dataframe.data_loader import DataLoader


class DatasetStream:
    def __init__(self, df):
        self.df = df

    def get_row_iterator(self):
        for i, row in self.df.iterrows():
            yield row
