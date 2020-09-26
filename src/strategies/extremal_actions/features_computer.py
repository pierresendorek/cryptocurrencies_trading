import numpy as np

from src.feature_engineering.local_linear_approximation_with_exponential_importance import LocalLinearApproximation
from src.feature_engineering.smoothing import ExponentialSmoother
from src.strategies.extremal_actions.finite_state_transducers import Features


class FeaturesComputer:
    def __init__(self, t_linear_prediction_long_term, t_linear_prediction_short_term):

        self.prev_time = None
        self.long_term_linear_predictor = LocalLinearApproximation(t_linear_prediction_long_term)
        self.long_term_sigma2_smooth = ExponentialSmoother(t_linear_prediction_long_term)
        self.short_term_linear_predictor = LocalLinearApproximation(t_linear_prediction_short_term)


    def compute(self, conversion_rate:float, time:float):
        if self.prev_time is None:
            self.prev_time = time - 1
            delta_t = 1
            long_term_linear_prediction_from_previous_values = conversion_rate
            short_term_linear_prediction_from_previous_values = conversion_rate

        else:
            delta_t = time - self.prev_time
            long_term_linear_prediction_from_previous_values = self.long_term_linear_predictor.pred_next_value(delta_t)
            short_term_linear_prediction_from_previous_values = self.short_term_linear_predictor.pred_next_value(delta_t)


        slope_long_term, offset = self.long_term_linear_predictor(conversion_rate, time)
        slope_short_term, offset = self.short_term_linear_predictor(conversion_rate, time)

        sigma2_prediction = self.long_term_sigma2_smooth(value=(conversion_rate - long_term_linear_prediction_from_previous_values) ** 2, delta_t=delta_t)
        abnormality = (conversion_rate - long_term_linear_prediction_from_previous_values) / (np.sqrt(sigma2_prediction) + 1E-20)

        features = Features(conversion_rate=conversion_rate,
                            long_term_smoothed_slope=slope_long_term,
                            short_term_smoothed_slope=slope_short_term,
                            long_term_linear_prediction_from_tendency=long_term_linear_prediction_from_previous_values,
                            short_term_linear_prediction_from_tendency=short_term_linear_prediction_from_previous_values,
                            sigma_2_prediction=sigma2_prediction,
                            time=time,
                            delta_time=delta_t,
                            prediction_error_abnormality=abnormality)

        self.prev_time = time
        return features