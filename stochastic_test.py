from matplotlib import pyplot as plt
from Functions import price_data_frame, time_converter
import MetaTrader5 as meta
from pandas_ta import stoch
from ta.trend import macd, macd_signal, sma_indicator
import numpy as np

bars = 400
dataframe = price_data_frame('GBPUSDm', meta.TIMEFRAME_M1, bars)
high = dataframe['high']
low = dataframe['low']
close = dataframe['close']
sma = sma_indicator(close, 14).tolist()
time = dataframe['time'].tolist()
stoch_line = stoch(high, low, close, 8, 3, 5)
kline = stoch_line['STOCHk_8_3_5'].tolist()
dline = stoch_line['STOCHd_8_3_5'].tolist()
macd_line = macd(close).tolist()
macd_signal_line = macd_signal(close).tolist()
line_chart = close.tolist()

line_chart.reverse()
kline.reverse()
dline.reverse()
time.reverse()
sma.reverse()

for i in (range(len(kline) - 2)):

    if line_chart[i+1] < sma[i+1]:
        if kline[i+2] > dline[i+2] and kline[i+1] < dline[i+1] and (kline[i+1] > 50):
            print('SELL : ', time_converter(time[i]))

    if line_chart[i+1] > sma[i+1]:
        if kline[i+2] < dline[i+2] and kline[i+1] > dline[i+1] and (kline[i+1] < 50):
            print('BUY  : ', time_converter(time[i]))
