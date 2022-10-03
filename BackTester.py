from matplotlib import pyplot as plt
from Functions import price_data_frame, rsi_crossover, speaker
import MetaTrader5 as meta
from ta.momentum import rsi

total_bars = 500 # Use larger values for great stochastic indicator
symbol = 'EURUSD'
df = price_data_frame(symbol, meta.TIMEFRAME_M1, total_bars)
rsi= rsi_crossover(df, total_bars)
current_rsi = rsi[0][0]
previous_rsi = rsi[1][0]
current_rsi_time = rsi[0][1]
previous_rsi_time = rsi[1][1]
time_difference = current_rsi_time - previous_rsi_time
if current_rsi == previous_rsi and time_difference <= 240:
    speaker('Market is ranging!', 3)
else:
    speaker('Market is trending!', 3)