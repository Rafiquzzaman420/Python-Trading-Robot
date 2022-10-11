from Functions import great_stochastic_indicator, initialization_check, price_data_frame, stochastic_indicator, time_converter, trend_detector
import MetaTrader5 as meta
import numpy as np

bars = 1440
# initialization_check()

dataframe = price_data_frame('EURUSD', meta.TIMEFRAME_M1, bars)

stochastic_indicator(dataframe, 8, 8, 3)
great_stochastic_indicator(dataframe)
signal = []
time_values = []
k_values, d_values,gk_values, gd_values = ([] for i in range(4))
for i in reversed(range(bars)):
    k_values.append(dataframe.at[i, '%K'])
    d_values.append(dataframe.at[i, '%D'])
    gk_values.append(dataframe.at[i, 'k_great'])
    gd_values.append(dataframe.at[i, 'd_great'])
    time_values.append(dataframe.at[i, 'time'])

for i in range(len(k_values)-2):
    if k_values[i+2] >= d_values[i+2] and k_values[i+1] <= d_values[i+1] and gd_values[i+1] >= 70:
        print('SELL : ', time_converter(time_values[i]))
    if k_values[i+2] <= d_values[i+2] and k_values[i+1] >= d_values[i+1] and gd_values[i+1] <= 30:
        print('BUY  : ', time_converter(time_values[i]))

# status = stochastic_crossover(dataframe, bars)
# status = trend_detector(dataframe, bars)
# np_array = np.array(status)
# size = np.shape(np_array)
# for i in range(size[0]):
#     print(status[i][0], time_converter(status[i][1]))