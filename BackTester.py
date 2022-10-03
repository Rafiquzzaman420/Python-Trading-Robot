from matplotlib import pyplot as plt
from Functions import great_stochastic_crossover, great_stochastic_indicator, price_data_frame, stochastic_crossover, time_converter
import MetaTrader5 as meta

total_bars = 500 # Use larger values for great stochastic indicator
symbol = 'EURUSD'
df = price_data_frame(symbol, meta.TIMEFRAME_M1, total_bars)
