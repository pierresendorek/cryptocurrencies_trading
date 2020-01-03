import numpy as np
from sortedcontainers import SortedDict
from numba import jitclass
from numba.typed import List
from numba import njit
from time import time
import pandas as pd
import gzip
import pickle

from src.feature_engineering.feature_engineering_with_market import FeatureEngineeringWithMarket

fe = FeatureEngineeringWithMarket()
df = pickle.load(gzip.open(fe.path_df_all_trades, "rb"))

print(list(df.columns))

