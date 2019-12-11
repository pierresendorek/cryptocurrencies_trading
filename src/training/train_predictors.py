from src.feature_engineering.old.feature_engineering_pipeline import FeatureEngineeringPipeline


class TrainPredictors:
    def __init__(self):
        self.feature_engineering = FeatureEngineeringPipeline()
        df_xbt = self.feature_engineering.transform()

        sep = (2 * len(df_xbt)) // 3


        self.df_train = {buy_or_sell: df_xbt[buy_or_sell].iloc[:sep]  for buy_or_sell in ["buy", "sell"]}
        self.df_test = {buy_or_sell: df_xbt[buy_or_sell].iloc[sep:]  for buy_or_sell in ["buy", "sell"]}

    def train(self):
        print(list(self.df_train["buy"].columns))
        print(list(self.df_train["sell"].columns))
        self.feature_engineering.feature_cols_list


train_predictors = TrainPredictors().train()






