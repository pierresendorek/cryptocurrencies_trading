import numpy as np
from datetime import timedelta, datetime
from numba import jit
from numba.typed import List



@jit
def rolling_max(x:np.ndarray, pos:np.ndarray, win_len:float):
    # is already anticausal
    r_m = np.zeros_like(x)
    position_value_list = List()
    minus_infinity_approximation = -1E30
    position_value_list.append((-1.0, minus_infinity_approximation))

    ix = x.shape[0] - 1
    while ix >= 0:
        while (len(position_value_list) > 0) and (x[ix] > position_value_list[-1][1]):
            position_value_list.pop(-1)
        position_value_list.append((pos[ix], x[ix]))
        while position_value_list[0][0] - pos[ix] > win_len:
            position_value_list.pop(0)
        r_m[ix] = position_value_list[0][1]
        ix -= 1
    return r_m



if __name__ == "__main__":
    N = 10**2
    x = np.random.rand(N)
    pos = np.linspace(1, N, N)

    from time import time
    time_start = time()
    r_m = rolling_max(x, pos, 100.0)
    time_end = time()
    print(time_end - time_start)

    import matplotlib.pyplot as plt
    plt.plot(x, linewidth=3)
    plt.plot(r_m)
    plt.show()