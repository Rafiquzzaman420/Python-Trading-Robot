from Functions import great_stochastic_crossover, price_data_frame, time_converter, stochastic_crossover
import MetaTrader5 as meta
import numpy as np

bars = 1440
dataframe = price_data_frame('EURUSDm', meta.TIMEFRAME_M1, bars)
stoch_cross = stochastic_crossover(dataframe, bars)
great_stoch_cross = great_stochastic_crossover(dataframe, bars)
great = np.array(great_stoch_cross)
great_size = np.shape(great)
small = np.array(stoch_cross)
small_size = np.shape(small)

for g in range(great_size[0]):
    for s in range(small_size[0]):
        time_difference = abs(great_stoch_cross[g][1] - stoch_cross[s][1]) / 60
        if great_stoch_cross[g][0] == 'buy' and stoch_cross[s][0] == 'buy' and \
            time_difference <= 15:
            print('BUY  : ', time_converter(great_stoch_cross[g][1]))
        if great_stoch_cross[g][0] == 'sell' and stoch_cross[s][0] == 'sell' and \
            time_difference <= 15:
            print('SELL : ', time_converter(great_stoch_cross[g][1]))
