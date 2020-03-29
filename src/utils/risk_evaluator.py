import numpy as np
from scipy.stats import norm




class RiskEvaluator:
    def __init__(self):
        pass

    def min_quantile_sum_gaussians(self, mu, sigma, quantile):
        assert quantile > 0.5
        b = norm.isf(quantile, loc=0, scale=sigma)
        return self.min_a_t_minus_b_sqrt_t(mu, b)

    def min_a_t_minus_b_sqrt_t(self, a, b):
        # b > 0
        # finds the minimum of f(t) = a * t - b * sqrt(t)
        t_min = (b / (2 * a)) ** 2
        value_of_minimum = a * t_min - b * np.sqrt(t_min)
        return value_of_minimum, t_min




if __name__ == "__main__":
    print(norm.isf(1-(1-0.9973)/2, loc=0.0, scale=1.0))

    import matplotlib.pyplot as plt

    x = np.linspace(0, 10, num=100)
    a = 3
    b = 5
    y = a * x - b * np.sqrt(x)

    y_min, x_min = RiskEvaluator().min_a_t_minus_b_sqrt_t(a,b)

    plt.plot(x, a * x, color='r')
    plt.plot(x, y)
    plt.scatter([x_min], [y_min])
    plt.show()
