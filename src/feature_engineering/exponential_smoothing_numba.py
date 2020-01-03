import numpy as np
from numba import njit, jitclass
from numba import float32
import matplotlib.pyplot as plt
from time import time


# TODO : put into a class to hide the internal variables
# TODO : make recursive
@njit
def _exponential_smooth_array(x, delta_t, times_to_divide_by_e):
    y = np.zeros((x.shape[0], times_to_divide_by_e.shape[0]))
    y_prev = 0.0
    for i_smoother in range(times_to_divide_by_e.shape[0]):
        y_prev = 0.0
        for it in range(x.shape[0]):
            a = - np.expm1(-delta_t[it] / times_to_divide_by_e[i_smoother]) #  1 - e^x
            y[it, i_smoother] = (1-a) * y_prev + a * x[it]
            y_prev = y[it, i_smoother]
    return y, y_prev


@njit
def _exponential_smooth_ones(delta_t, times_to_divide_by_e):
    y = np.zeros((delta_t.shape[0], times_to_divide_by_e.shape[0]))
    y_prev = 0.0
    for i_smoother in range(times_to_divide_by_e.shape[0]):
        y_prev = 0.0
        for it in range(x.shape[0]):
            a = - np.expm1(-delta_t[it] / times_to_divide_by_e[i_smoother])
            y[it, i_smoother] = (1-a) * y_prev + a
            y_prev = y[it, i_smoother]
    return y, y_prev


@njit
def _smooth_array(x, delta_t, times_to_divide_by_e):
    y, y_prec = _exponential_smooth_array(x, delta_t, times_to_divide_by_e)
    o, o_prec = _exponential_smooth_ones(delta_t, times_to_divide_by_e)
    return y/o, (y_prec, o_prec)


@jitclass(spec=[('times_to_divide_by_e', float32[:]),
                ('y_prev', float32),
                ('o_prev', float32)])
class ExponentialSmoother:
    def __init__(self, times_to_divide_by_e):
        self.times_to_divide_by_e = times_to_divide_by_e
        self.y_prev = 0.0
        self.o_prev = 0.0

    def smooth_array(self, x, delta_t):
        res, self.y_prev, self.o_prev = _smooth_array(x, delta_t, self.times_to_divide_by_e)
        return res


# usage example
if __name__ == "__main__":
    N = 10**5

    x = np.random.rand(N)  # > 0.999).astype(np.float64)
    delta_t = np.ones([N])
    times_to_divide_by_e = np.array([N/100.0, N/200.0, N/400.0, N/800.0][::-1])


    #start_time = time()
    #y = smooth_array(x, delta_t, time_to_divide_by_e)
    #y = buffer_processor(x, time_to_divide_by_e)
    #end_time = time()
    #print(end_time - start_time)


    start_time = time()
    y_full, y_prev = _smooth_array(x, delta_t, times_to_divide_by_e)
    end_time = time()
    print(end_time - start_time)

    print(y_prev)
    plt.plot(y_full)
    plt.show()

