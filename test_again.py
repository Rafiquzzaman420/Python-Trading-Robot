from matplotlib import pyplot as plt
from Functions import exponential_moving_average, price_data_frame, speaker, stochastic_crossover
import MetaTrader5 as meta
from ta.momentum import rsi

while True:
    bars = 1000
    dataframe = price_data_frame('GBPUSDm', meta.TIMEFRAME_M1, bars)
    dataframe['rsi'] = rsi(dataframe['close'], 14)
    rsi_list, fast_ma, slow_ma, current_time = ([] for i in range(4))
    exponential_moving_average(dataframe)
    stoch_list = stochastic_crossover(dataframe, bars)
    for i in (range(bars)):
        fast_ma.append(dataframe.at[i, 'Fast_EMA'])
        slow_ma.append(dataframe.at[i, 'Slow_EMA'])
        # Reverse current_time when in use
        current_time.append(dataframe.at[i, 'time'])

    current_time.reverse()
    time_difference = int(abs(current_time[0] - stoch_list[0][1]) / 60)

    if fast_ma[0] > slow_ma[0] and stoch_list[0][0] == 'buy' and time_difference <= 3:
        speaker('UP', 10)
    if fast_ma[0] < slow_ma[0] and stoch_list[0][0] == 'sell' and time_difference <= 3:
        speaker('DOWN', 10)
