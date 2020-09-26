from dataclasses import dataclass

from src.strategies.extremal_actions.context import Context


@dataclass
class Features:
    conversion_rate:float
    long_term_smoothed_slope:float
    short_term_smoothed_slope:float
    long_term_linear_prediction_from_tendency:float
    short_term_linear_prediction_from_tendency:float
    sigma_2_prediction:float
    time:float
    prediction_error_abnormality:float
    delta_time:float


@dataclass
class Params:
    time_to_wait_before_initialized:float
    mock_trades:bool
    abnormality_threshold:float


class Phase:
    def __call__(self, *args, **kwargs):
        raise NotImplemented


class Initialization(Phase):
    def __init__(self, params, context:Context):
        print("Initialization")
        self.init_time = None
        self.time_to_wait_before_initialized = params.time_to_wait_before_initialized
        self.params = params
        self.context = context

    def __call__(self, f:Features):
        if self.init_time is None:
            self.init_time = f.time

        if f.time - self.init_time < self.time_to_wait_before_initialized:
            return self
        else:
            return WaitForMinimum(self.params, self.context)


class WaitForMinimum(Phase):
    def __init__(self, params, context:Context):
        print("WaitForMinimum")

        self.abnormality_threshold = params.abnormality_threshold
        self.params = params
        self.context = context
        self.prev_slope = 1

    def __call__(self, f:Features):
        if self.prev_slope <= 0 and f.long_term_smoothed_slope > 0:
            return Buy(self.params, self.context)
        #elif f.prediction_error_abnormality < self.abnormality_threshold:
        #    return Buy(self.params, self.context)(f)
        else:
            self.prev_slope = f.long_term_smoothed_slope
            return self


class Buy(Phase):
    def __init__(self, params, context:Context):
        print("Buy")
        self.params = params
        self.context = context

    def __call__(self, f:Features):
        print("Wallet ", self.context.wallet._repr_(f.conversion_rate))
        self.context.enqueue_action_buy(f.conversion_rate)
        return WaitForProfitableMoment(self.params, self.context)


class WaitForProfitableMoment(Phase):
    def __init__(self, params, context:Context):
        print("WaitForProfitableMoment")
        self.params = params
        self.context = context
        self.prev_slope = -1

    def __call__(self, f:Features):
        #if self.prev_slope >= 0 and f.long_term_smoothed_slope < 0 and \
        if self.context.has_profitable_investment(f.conversion_rate):
            return Sell(self.params, self.context)(f)
        else:
            self.prev_slope = f.long_term_smoothed_slope
            return self


class Sell(Phase):
    def __init__(self, params, context):
        print("Sell")
        self.params = params
        self.context = context

    def __call__(self, f:Features):
        print("Wallet ", self.context.wallet._repr_(f.conversion_rate))
        self.context.enqueue_action_sell(conversion_rate=f.conversion_rate)
        return WaitForMinimum(self.params, self.context)









