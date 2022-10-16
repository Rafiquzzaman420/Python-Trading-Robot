from Functions import great_stochastic_indicator, price_data_frame, stochastic_indicator, time_converter, stochastic_crossover, great_stochastic_crossover
import MetaTrader5 as meta
import numpy as np

bars = 1440
dataframe = price_data_frame('EURUSDm', meta.TIMEFRAME_M1, bars)
small = stochastic_indicator(dataframe, 8, 3, 8)
big = great_stochastic_indicator(dataframe)
k_values, d_values, gk_values, gd_values, time = ([] for i in range(5))
for i in reversed(range(bars)):
    k_values.append(dataframe.at[i, '%K'])
    d_values.append(dataframe.at[i, '%D'])
    gk_values.append(dataframe.at[i, 'k_great'])
    gd_values.append(dataframe.at[i, 'd_great'])
    time.append(dataframe.at[i, 'time'])

for i in range(bars -2):
    if k_values[i+2] < d_values[i+2] and k_values[i+1] > d_values[i+1] \
        and k_values[i+1] <= 25 and gk_values[i+1] < 30 and gd_values[i+1] < 35:
        print('BUY : ',time_converter(time[i]))
    if k_values[i+2] > d_values[i+2] and k_values[i+1] < d_values[i+1] \
        and k_values[i+1] >= 75 and gk_values[i+1] > 70 and gd_values[i+1] > 65:
        print('SELL : ',time_converter(time[i]))
