from math import sqrt, exp
from numpy import log as ln, exp, mean, std, var
from scipy.stats import norm
import pandas as pd

def n_func(d):
    return norm.cdf(d)

class GeomBasket:
    def __init__(self):
        pass

    def closed_form_solution_price(self, S1, S2, sigma1, sigma2, K, r, T, rho, optionType):
        sigma_B = sqrt(sigma1**2 + 2*sigma1*sigma2*rho + sigma2**2)/2
        mu = r - 0.5*((sigma1**2 + sigma2**2)/2) + 0.5*sigma_B**2
        Bg = sqrt(S1*S2)
        d1 = (ln(Bg/K) + (mu + 0.5*sigma_B**2)*T)/(sigma_B*sqrt(T))
        d2 = d1 - sigma_B*sqrt(T)
        if(optionType.lower()=='call'):
            geo_basket_call = exp(-r*T)*(Bg*exp(mu*T)*n_func(d1) - K*n_func(d2))
            return geo_basket_call
        geo_basket_put = exp(-r*T)*(K*n_func(-d2) - Bg*exp(mu*T)*n_func(-d1))
        return geo_basket_put

# S1 = 100
# S2 = 100
# r = 0.05
# T = 3
#
# test_cases_basket = {'K':[100, 100, 100, 80, 120, 100, 100, 100, 100, 80, 120, 100],
#                      'sigma1': [0.3, 0.3, 0.1, 0.3, 0.3, 0.5, 0.3, 0.3, 0.1, 0.3, 0.3, 0.5],
#                      'sigma2': [0.3, 0.3, 0.3, 0.3, 0.3, 0.5, 0.3, 0.3, 0.3, 0.3, 0.3, 0.5],
#                      'rho': [0.5, 0.9, 0.5, 0.5, 0.5, 0.5, 0.5, 0.9, 0.5, 0.5, 0.5, 0.5],
#                      'optionType':['Put','Put','Put','Put','Put','Put','Call','Call','Call','Call','Call','Call']}
#
# TC_basket = pd.DataFrame(test_cases_basket)
# gb = GeomBasket()
#
# for index, row in TC_basket.iterrows():
#     sigma1 = row['sigma1']
#     sigma2 = row['sigma2']
#     K = row['K']
#     rho = row['rho']
#     optionType = row['optionType']
#     geoBasket_px = gb.closed_form_solution_price(S1, S2, sigma1, sigma2, K, r, T, rho, optionType)
#     print("If sigma1 = %.2f; sigma2 = %.2f; rho = %.2f; K = %d; options = %s; geometric basket option price = %.3f" % (sigma1, sigma2, rho, K, optionType, geoBasket_px))