### 7. The Binomial Tree method for American call/put options
import numpy as np
from math import sqrt, exp


class AmericanOption:
    def __init__(self, S=None, K=None, T=0, sigma=None, r=0.0, N=200, option_type=None):
        assert option_type.lower() == 'call' or option_type.lower() == 'put'
        self.S = S
        self.K = K
        self.T = T
        self.sigma = sigma
        self.r = r
        self.N = N
        self.option_type = option_type

    def bi_tree_pricing(self):
        S, K, T, sigma, N, r, option_type = self.S, self.K, self.T, self.sigma, self.N, self.r, self.option_type

        dt = T / N
        u = exp(sigma * sqrt(dt))
        d = exp(-sigma * sqrt(dt))
        drift = exp(r * dt)
        p = (drift - d) / (u - d)

        stk_price_tree = np.zeros((N + 1, N + 1))
        stk_price_tree[0, 0] = S
        for i in range(1, N + 1):
            stk_price_tree[i, 0] = stk_price_tree[i - 1, 0] * u
            for j in range(1, i + 1):
                stk_price_tree[i, j] = stk_price_tree[i - 1, j - 1] * d

        option_val = np.zeros((N + 1, N + 1))
        for i in range(N + 1):
            if option_type.lower() == 'call':
                option_val[N, i] = max(0, stk_price_tree[N, i] - K)
            else:
                option_val[N, i] = max(0, K - stk_price_tree[N, i])
        for i in range(N - 1, -1, -1):
            for j in range(i + 1):
                option_val[i, j] = (p * option_val[i + 1, j] + (1 - p) * option_val[i + 1, j + 1]) / drift
                if option_type.lower() == 'call':
                    option_val[i, j] = max(option_val[i, j], stk_price_tree[i, j] - K)
                else:
                    option_val[i, j] = max(option_val[i, j], K - stk_price_tree[i, j])
        return option_val[0, 0]


# S = 50
# K = 40
# sigma = 0.4
# r = 0.1
# T = 2
# N = 200
# optionType = "Put"

# a = AmericanOption(50,40,2, 0.4,0.1,200,"put")
# print(a.bi_tree_pricing())

# american_px = bi_tree_pricing(S, K, sigma, r, T, N, optionType)
# print("American vanilla price is: %.5f" % american_px)
