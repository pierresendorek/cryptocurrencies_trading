from time import time
from datetime import timedelta

def time_execution(f, *args, **kwargs):
    t0 = time()
    res = f(*args, **kwargs)
    duration = time() - t0
    return res, duration

nesting_level = 0

# decorator
def print_execution_time(func):
    def wrapper(*args, **kwargs):
        global nesting_level
        print(" " * 4 * nesting_level + "Starting ", func.__name__)
        nesting_level +=1
        res, duration = time_execution(func, *args, **kwargs)
        nesting_level -=1
        print(" " * 4 * nesting_level + "Done : ", func.__name__, " took ", str(timedelta(seconds=duration)))
        return res
    return wrapper




if __name__ == "__main__":

    @print_execution_time
    def f(x):
        s = 0
        for i in range(3):
            s += g(x)

    @print_execution_time
    def g(x):
        return x * x

    print(f(3))


