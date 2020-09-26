import numpy as np

class Weights:
    def __init__(self, gamma):
        self.prev_W = 1.0
        self.prev_time = None
        self.gamma = gamma

    def __call__(self, value, time):
        if self.prev_time is None:
            self.prev_time = time - 1

        e = np.exp(self.gamma * (self.prev_time - time))
        W = 1 +  e * self.prev_W
        self.prev_W = W
        self.prev_time = time
        return W, e


class TimeDifferences:
    def __init__(self):
        self.prev_T = 0
        self.prev_time = None

    def __call__(self, value, time, prev_W, e):
        if self.prev_time is None:
            self.prev_time = time - 1

        T = e * (self.prev_T + prev_W * (self.prev_time - time))
        self.prev_T = T
        self.prev_time = time
        return T


class Values:
    def __init__(self):
        self.prev_Y = 0
        self.prev_time = None

    def __call__(self, value, time, e):
        if self.prev_time is None:
            self.prev_Y = value
            self.prev_time = time - 1

        Y = value + e * self.prev_Y
        self.prev_Y = Y
        self.prev_time = time
        return Y


class SquaredTimeDifferences:
    def __init__(self):
        self.prev_S = 0.0
        self.prev_time = None

    def __call__(self, value, time, prev_W, prev_T, e):
        if self.prev_time is None:
            self.prev_time = time - 1

        S = e * (self.prev_S + 2 * prev_T * (self.prev_time - time) + prev_W * (self.prev_time - time) ** 2)
        self.prev_S = S
        self.prev_time = time
        return S


class TimeValueProduct:
    def __init__(self):
        self.prev_time = None
        self.prev_P = 0

    def __call__(self, value, time, prev_Y, e):
        if self.prev_time is None:
            self.prev_time = time - 1
        P = e * (self.prev_P + (self.prev_time - time) * prev_Y)
        self.prev_P = P
        self.prev_time = time
        return P


class LocalLinearApproximation:
    def __init__(self, time_to_divide_by_e):
        gamma = 1/time_to_divide_by_e
        self.W = Weights(gamma)
        self.T = TimeDifferences()
        self.Y = Values()
        self.P = TimeValueProduct()
        self.S = SquaredTimeDifferences()
        self.prev_e = 1.0
        self.prev_hat_a = None
        self.prev_hat_b = None

    def __call__(self, value, time):
        prev_W = self.W.prev_W
        prev_T = self.T.prev_T
        prev_Y = self.Y.prev_Y


        W, e = self.W(value, time)

        T = self.T(value, time, prev_W, e)
        Y = self.Y(value, time, e)
        S = self.S(value, time, prev_W, prev_T, e)
        P = self.P(value, time, prev_Y, e)

        barY = Y / W
        barT = T / W

        den_a = S - W * barT**2
        num_a = P -  barY * barT * W

        hat_a = num_a / den_a

        hat_b = barY - hat_a * barT

        self.prev_hat_a = hat_a
        self.prev_hat_b = hat_b

        return hat_a, hat_b

    def pred_next_value(self, detla_t):
        if self.prev_hat_a is None:
            return None
        else:
            return self.prev_hat_a * detla_t + self.prev_hat_b




if __name__ == "__main__":
    import numpy as np
    import matplotlib.pyplot as plt

    step = 2 * np.pi / 100

    N = 100000
    v1 = np.random.randn(N) * 10
    v2 = np.random.randn(N) * 10 + 60
    b = (np.random.rand(N) > 0.5).astype(np.float)
    t = v1 * b + (1-b) * v2

    t = np.array(np.sort(t))

    y_no_noise = np.sin(t)  + np.exp(-t*t/200)


    y = y_no_noise + np.random.randn(len(t)) / 1000

    y_prime = (y[1:] - y[:-1]) / (t[1:] - t[:-1])
    y_no_noise_prime = (y_no_noise[1:] - y_no_noise[:-1]) / (t[1:] - t[:-1])

    F = LocalLinearApproximation(time_to_divide_by_e=0.5)
    a_list = []

    time_prev = 0
    for i, value in enumerate(y):
        F(value, t[i])
        if i >= 1:
            a = F.pred_next_value(t[i] - time_prev)
        else:
            a = 0

        a_list.append(a)
        time_prev = t[i]



    #plt.plot(t[1:],y_prime)
    plt.plot(t, y)
    plt.plot(t, y_no_noise)

    plt.plot(t, a_list)
    #plt.plot(t[1:], y_no_noise_prime)

    plt.show()





