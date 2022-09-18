import MetaTrader5 as meta
import pandas as pd
from mplfinance.original_flavor import candlestick_ohlc
import numpy as np
import matplotlib.pyplot as plt

def initialization_check():
    if not meta.initialize():
        print('Initialization failed.\nError code : ', meta.last_error())
        quit()

def price_data_frame(symbol, time_frame, total_bars):
    initialization_check()
    # Retrieving previous bar positions (Open, High, Low, Close, Tick Volume)
    price_rates = meta.copy_rates_from_pos(symbol, time_frame, 0, total_bars)
    meta.shutdown()
    # Converting into an easy-to-read pandas data frame
    data_frame = pd.DataFrame(price_rates)
    # Converting time
    # data_frame['time'] = pd.to_datetime(data_frame['time'], unit='s')
    return data_frame


def stochastic_indicator(dataframe, k, d, slow):
    close = dataframe['close']
    low = dataframe['low'].rolling(k).min()
    high = dataframe['high'].rolling(k).max()
    dataframe['%K_Fast'] = (close - low) * 100 / (high - low)
    dataframe['%K'] = dataframe['%K_Fast'].rolling(slow).mean()
    dataframe['%D'] = dataframe['%K'].rolling(d).mean()
    # axis = dataframe[['%K', '%D']].plot()
    # axis.axhline(20, linestyle='--', color="r")
    # axis.axhline(80, linestyle="--", color="r")
    # plt.show()
    return dataframe['%K'], dataframe['%D']


def exponential_moving_average(dataframe, fast=21, slow=200):
    dataframe['Fast_EMA'] = dataframe['close'].ewm(span=fast, adjust=False).mean()
    dataframe['Slow_EMA'] = dataframe['close'].ewm(span=slow, adjust=False).mean()
    return dataframe['Fast_EMA'], dataframe['Slow_EMA']


def ema_crossover_detection(dataframe):
    exponential_moving_average(dataframe)
    fast_ema = []
    slow_ema = []
    for info in reversed(range(799, 999)):
        fast_ema.append(dataframe.at[info, 'Fast_EMA'])
        slow_ema.append(dataframe.at[info, 'Slow_EMA'])


def stochastic_crossover_detection(dataframe):
    stochastic_indicator(dataframe, 21, 3, 7)
    k_line = []  # Fast Line
    d_line = []  # Slow Line
    for info in reversed(range(799, 999)):
        k_line.append(dataframe.at[info, '%K'])
        d_line.append(dataframe.at[info, '%D'])
    if k_line[1] > d_line[1] and k_line[0] < d_line[0]:
        return 'Crossover Detected. BUY'
    if k_line[1] < d_line[1] and k_line[0] > d_line[0]:
        return 'Crossover Detected. SELL'
    if k_line[0] < d_line[0] and k_line[1] <= 25 or d_line[1] <= 25:
        return 'BUY'
    if k_line[0] > d_line[0] and k_line[1] >= 75 or d_line[1] >= 75:
        return 'SELL'

def is_support(df,i):  
  cond1 = df['low'][i] < df['low'][i-1]   
  cond2 = df['low'][i] < df['low'][i+1]   
  cond3 = df['low'][i+1] < df['low'][i+2]   
  cond4 = df['low'][i-1] < df['low'][i-2]  
  return (cond1 and cond2 and cond3 and cond4) 

# determine bearish fractal
def is_resistance(df,i):  
  cond1 = df['high'][i] > df['high'][i-1]   
  cond2 = df['high'][i] > df['high'][i+1]   
  cond3 = df['high'][i+1] > df['high'][i+2]   
  cond4 = df['high'][i-1] > df['high'][i-2]  
  return (cond1 and cond2 and cond3 and cond4)

# to make sure the new level area does not exist already
def is_far_from_level(value, levels, df, tuner):
  # tuner = 0.001 # 1 Minute : 0.001, 1 Hour : 0.004
  ave =  np.mean((df['high'] - df['low'])) + tuner
  return np.sum([abs(value-level)<ave for _,level in levels])==0

# Store Horizontal level information
def store_levels(data_frame, level, tuner):
  # Use this function to store level data
  for i in range(2, data_frame.shape[0] - 2):  
    if is_support(data_frame, i):    
      low = data_frame['low'][i]    
      if is_far_from_level(low, level, data_frame, tuner):      
        level.append((i, low))  
    elif is_resistance(data_frame, i):    
      high = data_frame['high'][i]    
      if is_far_from_level(high, level, data_frame, tuner):      
        level.append((i, high))

# For human visualization
def plotter(levels, df):    
  fig, ax = plt.subplots(figsize=(150, 60))
  candlestick_ohlc(ax,df.values,width=30, colorup='green', 
    colordown='red', alpha=1)
  for level in levels:
    plt.hlines(level[1], xmin = df['time'][level[0]], xmax = 
      max(df['time']), colors='blue', linestyle='-')
  fig.show()

def horizontal_line_values(hline_values, hline_output_values):
# Return values of levels in list format
  for i in range(len(hline_values)):
    value = hline_values[i] # [(13, 1.00002)]
    line_values = list(value) # [13, 1.00002]
    hline_output_values.append(line_values)
  return hline_output_values

def horizontal_line_position(total_bars, hline_output, data_frame, differnece, hline_position):
    current_position = data_frame.at[total_bars - 1, 'close']
    above, below = 1, -1
    for i in range(len(hline_output)):
        diff = abs(current_position - hline_output[i][1])
        differnece.append(diff)
        hline_position.append([diff, hline_output[i][1]])

    differnece = min(differnece)
    x = [x for x in hline_position if differnece in x][0]
    position = hline_position.index(x)
    hline_position = hline_position[position][1]
    if current_position - hline_position > 0:
        return hline_position, above
    else:
        return hline_position, below