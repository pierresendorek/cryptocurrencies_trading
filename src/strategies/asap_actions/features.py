from dataclasses import dataclass

from src.feature_engineering.local_linear_approximation_with_exponential_importance import LocalLinearApproximation
from src.feature_engineering.smoothing import ExponentialSmoother
import numpy as np

@dataclass
class Features:
    conversion_rate:float
    time:float
    smoothed_log_conversion_rate:float
    smoothed_sigma2_of_log:float
    slope_of_log_conversion_rate:float
    prev_slope_of_log_conversion_rate:float


class FeaturesComputer:
    def __init__(self, smoothing_time, slope_time):
        self.conversion_rate_smoother = ExponentialSmoother(time_to_divide_by_e=smoothing_time)
        self.sigma2_smoother = ExponentialSmoother(time_to_divide_by_e=smoothing_time)
        self.prev_time = None
        self.local_linear_approximator = LocalLinearApproximation(slope_time)

    def __call__(self, conversion_rate, time):
        if self.prev_time is None:
            self.prev_time = time - 1
            self.prev_slope = 0.0

        delta_t = time - self.prev_time
        log_conversion_rate = np.log(conversion_rate)
        smoothed_log_conversion_rate = self.conversion_rate_smoother(log_conversion_rate, delta_t)
        smoothed_sigma2_of_log = self.sigma2_smoother((log_conversion_rate - smoothed_log_conversion_rate)**2, delta_t)
        slope, _ = self.local_linear_approximator(log_conversion_rate, time)
        features = Features(conversion_rate, time, smoothed_log_conversion_rate, smoothed_sigma2_of_log, slope, self.prev_slope)
        self.prev_slope = slope
        return features

