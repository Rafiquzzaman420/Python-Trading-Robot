from matplotlib import pyplot as plt
from Functions import price_data_frame, time_converter
import MetaTrader5 as meta
from ta.utils import _sma
from pandas_ta import rsi

bars = 200
dataframe = price_data_frame('GBPUSDm', meta.TIMEFRAME_M1, bars)
close = dataframe['close']
time = dataframe['time'].tolist()
rsi_line = rsi(close, 14)
rsi_sma = _sma(rsi_line, 14).tolist()
rsi_line = rsi_line.tolist()
time.reverse()
rsi_line.reverse()
rsi_sma.reverse()
j = 0
for i in range(len(rsi_sma) - 2):
    if rsi_line[i+2] < rsi_sma[i+2] and rsi_line[i+1] > rsi_sma[i+1]:
        j += 1
        print(f'{j}. BUY  : ', time_converter(time[i]))
    if rsi_line[i+2] > rsi_sma[i+2] and rsi_line[i+1] < rsi_sma[i+1]:
        j += 1
        print(f'{j}. SELL : ', time_converter(time[i]))


# Observation 1

# When RSI is signaling down which means the rsi line is below the sma line
# and after that the stochastic signaling down too, then the market will
# go down. But when RSI is signaling up (means when the RSI line is above the sma line)
# and stochastic signals up, then market will go up.

# Observation 2

# When RSI sma line is below the 50 line, market is in down trend (definitely) and if
# stochastic indicates down, market will go down. When RSI sma line is above the 50 line
# and stochastic indicates up, then market will go up.