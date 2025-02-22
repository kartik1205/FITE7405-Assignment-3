from math import sqrt, exp
from numpy import log as ln, exp, mean, std, var
from scipy.stats import norm
from BlackScholes import BlackScholes


def n_func(d):
    return norm.cdf(d)


# 3. Implement closed-form formulas for geometric Asian call/put options
class GeomAsian:
    def __init__(self, S=None, K=None, T=0, sigma=None, r=0.0, n=100, option_type=None):
        assert option_type.lower() == 'call' or option_type.lower() == 'put'
        self.S = S
        self.K = K
        self.T = T
        self.sigma = sigma
        self.r = r
        self.n = n
        self.option_type = option_type

    def closed_form_solution_price(self):
        S, K, sigma, r, T, N, optionType = self.S, self.K, self.sigma, self.r, self.T, self.n, self.option_type
        sigma_hat = sigma * sqrt((N + 1) * (2 * N + 1) / (6 * N * N))
        mu = (r - 0.5 * sigma ** 2) * ((N + 1) / (2 * N)) + 0.5 * sigma_hat ** 2
        d1 = ((ln(S / K) + (mu + 0.5 * sigma_hat ** 2)) * T) / (sigma_hat * sqrt(T))
        d2 = d1 - sigma_hat * sqrt(T)
        if optionType.lower() == 'call':
            geo_call = exp(-r * T) * (S * exp(mu * T) * n_func(d1) - K * n_func(d2))
            return geo_call
        geo_put = exp(-r * T) * (K * n_func(-d2) - S * exp(mu * T) * n_func(-d1))
        return geo_put

# S = 100
# K = 100
# r = 0.05
# T = 3
# sigma = 0.3
# n=50
# optionType ="put"
#
# bs = BlackScholes()


# parameter = [
#     {"sigma":0.3, "n":50, "optionType":"put"},
#     {"sigma":0.3, "n":100, "optionType":"put"},
#     {"sigma":0.4, "n":50, "optionType":"put"},
#     {"sigma":0.3, "n":50, "optionType":"call"},
#     {"sigma":0.3, "n":100, "optionType":"call"},
#     {"sigma":0.4, "n":50, "optionType":"call"}
# ]
#
# for params in parameter:
#     sigma = params["sigma"]
#     n = params["n"]
#     optionType = params["optionType"]
#     ga = GeomAsian(S,K, T,sigma,r,n,optionType)
#     geoAsian_px = ga.closed_form_solution_price()
#     print("sigma = %.2f; n = %d; options type = %s; geometric asian option price is %.3f" %(sigma, n, optionType, geoAsian_px))
#     vanilla_px = bs.euro_extended(S, K, T, r, 0, sigma, optionType)
#     print("Black-Scholes price: %.3f" %vanilla_px)

# geoAsian_px = ga.closed_form_solution_price(S, K, sigma, r, T, n, optionType)
