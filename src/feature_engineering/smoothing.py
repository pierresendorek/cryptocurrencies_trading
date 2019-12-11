import numpy as np
from datetime import timedelta, datetime

def exponential_range(start, end, nb_subdiv):
    return np.exp(np.linspace(np.log(start), np.log(end), nb_subdiv))


class RollingMaxCausal:
    def __init__(self, win_len):
        self.position_value_list = [(-1, -float("inf"))]
        self.win_len = win_len

    def get_next(self, i, x):
        while len(self.position_value_list) > 0 and x > self.position_value_list[-1][1]:
            self.position_value_list.pop(-1)
        self.position_value_list.append((i, x))
        while i - self.position_value_list[0][0] > self.win_len:
            self.position_value_list.pop(0)
        return self.position_value_list[0][1]

from typing import List, Tuple

class RollingMaxAnticausal:
    def __init__(self, win_len:timedelta):
        self.position_value_list: List[Tuple[datetime, float]] = [(datetime(1970, 1, 1), -float("inf"))]
        self.win_len = win_len

    def get_next(self, i:datetime, x):
        while len(self.position_value_list) > 0 and x > self.position_value_list[-1][1]:
            self.position_value_list.pop(-1)
        self.position_value_list.append((i, x))
        while self.position_value_list[0][0] - i > self.win_len:
            self.position_value_list.pop(0)
        return self.position_value_list[0][1]


class ExponentialSmoother:
    def __init__(self, time_to_divide_by_e):
        self.num = 0.0
        self.den = 0.0
        self.time_to_divide_by_e = time_to_divide_by_e  # seconds

    def get_next(self, value, delta_t):
        a = np.exp(-delta_t / self.time_to_divide_by_e)
        self.num = a * self.num + (1 - a) * value #* delta_t
        self.den = a * self.den + (1 - a) #* delta_t
        return self.num / self.den

    def __repr__(self):
        return "ExponentialSmoother(" + str(self.time_to_divide_by_e) +")"


class MultipleExponentialSmoother:
    def __init__(self, time_to_divide_by_e_list: list):
        time_to_divide_by_e_array = np.array(time_to_divide_by_e_list)
        self.dim = len(time_to_divide_by_e_array)
        self.num = np.ones([self.dim]) * 1E-16
        self.den = np.ones([self.dim]) * 1E-16
        self.time_to_divide_by_e_array = time_to_divide_by_e_array

    def get_next(self, value, delta_t):
        a = np.exp(-delta_t / self.time_to_divide_by_e_array)
        self.num = a * self.num + (1 - a) * value  # * delta_t
        self.den = a * self.den + (1 - a)  # * delta_t
        return self.num / self.den

    def __repr__(self):
        return "MultipleExponentialSmoother(" + str(self.time_to_divide_by_e_array) +")"



if __name__ == "__main__":
    ms = MultipleExponentialSmoother([1,2,4,8])
    print(ms.get_next(1.0, 1.0))
    print(ms.get_next(0.0, 1.0))
    print(ms.get_next(0.0, 1.0))