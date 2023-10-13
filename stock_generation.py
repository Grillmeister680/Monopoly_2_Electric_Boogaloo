import random
import numpy as np
import pandas as pd
from statistics import NormalDist
import math

counter = 0
price_ts = [1]
returns = []
e = 2.7182818284590452353602874713527
pi = 3.141592653589793238462643383279502884197

while counter < 300:
    condition = random.randint(1, 10)
    if condition <=6:
        #normal
        r_ts = [0]

        for i in range(6):
            mu, sigma = 0.01, 0.02
            r = 0.1 * r_ts[-1] +  np.random.normal(mu, sigma)
            r_ts.append(r)
        r_ts.pop(0)
        for j in r_ts:
            price = price_ts[-1] * (1 + j)
            counter = counter + 1
            returns.append((price - price_ts[-1])/price_ts[-1])
            price_ts.append(price)

    if condition >= 9:
        #recession
        r_ts = [0]
        for i in range(4):
            mu, sigma = -0.02, 0.03
            r = 0.1 * r_ts[-1] +  np.random.normal(mu, sigma)
            r_ts.append(r)
        r_ts.pop(0)
        for j in r_ts:
            price = price_ts[-1] * (1 + j)
            counter = counter + 1  
            returns.append((price - price_ts[-1])/price_ts[-1])  
            price_ts.append(price)

    else:
        #boom
        r_ts = [0]
        for i in range(4):
            mu, sigma = 0.03, 0.03
            r = 0.1 * r_ts[-1] +  np.random.normal(mu, sigma)
            r_ts.append(r)
        r_ts.pop(0)
        for j in r_ts:
            price = price_ts[-1] * (1 + j)
            counter = counter + 1    
            returns.append((price - price_ts[-1])/price_ts[-1])
            price_ts.append(price)

rate = [0.0075]
rate_normal = 0.0075
rate_recession = 0
rate_boom = 0.025
for k in returns:
    weight_normal = math.tan(NormalDist().pdf((k-0.01)/0.02)*pi/0.95)
    weight_recession = math.tan(NormalDist().pdf((k+0.02)/0.03)*pi/0.95)
    weight_boom = math.tan(NormalDist().pdf((k-0.03)/0.03)*pi/0.95)
    sum_weights = weight_normal + weight_recession + weight_boom
 
    p_normal = weight_normal / sum_weights
    p_boom = weight_boom / sum_weights

    interest_rate = p_normal * rate_normal + p_boom * rate_boom
    if interest_rate < 0:
        interest_rate = 0
    rate.append(interest_rate)

invest_bonds = [1]
for l in rate:
    invest_bonds.append(invest_bonds[-1] * (1 + l))
invest_bonds.pop(-1)

df = pd.DataFrame(
    {'price': price_ts, 
     'bond investor': invest_bonds,
     'federal funds rate': rate})
df.to_excel("stock_price.xlsx")
