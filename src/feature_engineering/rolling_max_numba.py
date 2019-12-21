import numpy as np
from datetime import timedelta, datetime
from numba import jit
from numba.typed import List

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


@jit
def rolling_max(x, pos, win_len):

    r_m = np.zeros_like(x)
    position_value_list = List()
    position_value_list.append((-1.0, -1E30))

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
    N = 10**7
    x = np.random.rand(N)
    pos = np.linspace(1, N, N)

    from time import time
    time_start = time()
    r_m = rolling_max(x, pos, 1000.0)
    time_end = time()
    print(time_end - time_start)

    #plt.plot(x)
    #plt.plot(r_m)
    #plt.show()