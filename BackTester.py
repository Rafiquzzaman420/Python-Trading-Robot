import MetaTrader5 as meta
from Functions import price_data_frame, horizontal_lines, store_levels, plotter

TOTAL_BARS = 1000

symbol = 'EURUSDm'
df = price_data_frame(TOTAL_BARS, meta.TIMEFRAME_H1, symbol)

#method 1: fractal candlestick pattern
# determine bullish fractal 

# a list to store resistance and support levels
levels = []
tuner = 0.001
store_levels(df, levels, tuner)

plotter(levels, df)

print(horizontal_lines(levels))