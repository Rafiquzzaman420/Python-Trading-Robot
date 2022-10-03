import MetaTrader5 as meta
from math import floor, ceil
import pandas as pd
from mplfinance.original_flavor import candlestick_ohlc
import numpy as np
import matplotlib.pyplot as plt
import time
from pygame import mixer
from ta.momentum import williams_r,rsi
from ta.trend import adx_pos, adx_neg, adx
from datetime import datetime
import win32com.client

def speaker(message, repeat):
  speaker = win32com.client.Dispatch("SAPI.SpVoice")
  for i in range(repeat):
    speaker.Speak(message)

def initialization_check():
    if not meta.initialize():
        print('Initialization failed.\nError code : ', meta.last_error())
        quit()

def time_detector(dataframe, total_bars):
    std_time = 1661968800 + 6*60*60
    current_time = []
    for i in reversed(range(total_bars)):
      dataframe_time = dataframe.at[i, 'time']
      current_time.append(dataframe_time + 6*60*60)

    difference = (current_time[1]- std_time)
    if difference > 86400:
        alpha = floor(difference / 86400)
        difference = floor((difference - (86400 * alpha)) / 3600)
        return difference
    if difference < 86400:
      difference = floor(difference / 3600)
      return difference

def time_converter(unix_time):
  normal_time = datetime.utcfromtimestamp(unix_time).strftime('%Y-%m-%d %H:%M:%S')
  return normal_time

def williams_r_crossover(dataframe, total_bars):
  period = 14
  williams_r_list = []
  signal = []
  high = dataframe['high']
  low = dataframe['low']
  close = dataframe['close']
  time_values = []
  dataframe['wpr'] = williams_r(high, low, close, period)
  for i in reversed(range(total_bars)):
    williams_r_list.append(dataframe.at[i, 'wpr'])
    time_values.append(dataframe.at[i, 'time'])

  for i in range(len(williams_r_list)-2):
    if williams_r_list[i+1] >= -11:
      signal.append(['sell', time_values[i+1]])
    if williams_r_list[i+1] <= -89:
      signal.append(['buy', time_values[i+1]])

  return signal

def adx_crossover(dataframe, bars):
  adx_list = []
  time_values = []
  signal = []
  dataframe['adx'] = adx(dataframe['high'], dataframe['low'], dataframe['close'])
  dataframe['adx_pos'] = adx_pos(dataframe['high'], dataframe['low'], dataframe['close'])
  dataframe['adx_neg'] = adx_neg(dataframe['high'], dataframe['low'], dataframe['close'])
  for i in reversed(range(bars)):
    adx_list.append([dataframe.at[i, 'adx'], dataframe.at[i, 'adx_pos'], dataframe.at[i, 'adx_neg']])
    time_values.append(dataframe.at[i, 'time'])
  # TODO : Need to work on the logic here!
  for i in range(len(adx_list) - 1):
    if adx_list[i+1][0] >= 25 and adx_list[i+1][1] >= adx_list[i+1][2]:
      signal.append('TREND_UP', time_values[i+1])

    if adx_list[i+1][0] >= 25 and adx_list[i+1][2] >= adx_list[i+1][1]:
      signal.append('TREND_DOWN', time_values[i+1])  

def rsi_crossover(dataframe, bars):
  rsi_list = []
  time_values = []
  signal = []
  dataframe['rsi'] = rsi(dataframe['close'])
  for i in reversed(range(bars)):
    rsi_list.append(dataframe.at[i, 'rsi'])
    time_values.append(dataframe.at[i, 'time'])
  
  for i in range(len(rsi_list) - 2):
    if floor(rsi_list[i+2]) <= 35 and floor(rsi_list[i+1]) >= 35:
      signal.append('buy', time_values[i+1])
    if ceil(rsi_list[i+2]) >= 65 and ceil(rsi_list[i+1]) <= 65:
      signal.append('sell', time_values[i+1])
  return signal

def stochastic_crossover(dataframe, total_bars):
  stochastic_indicator(dataframe)
  signal = []
  time_values = []
  k_values, d_values = ([] for i in range(2))
  for i in reversed(range(total_bars)):
    k_values.append(dataframe.at[i, '%K'])
    d_values.append(dataframe.at[i, '%D'])
    time_values.append(dataframe.at[i, 'time'])
  for i in range(len(k_values)-2):
    if k_values[i+2] >= d_values[i+1] and k_values[i+1] <= d_values[i+1] and k_values[i+1] >= 75:
      signal.append(['sell', time_values[i+1]])
    if k_values[i+2] <= d_values[i+1] and k_values[i+1] >= d_values[i+1] and k_values[i+1] <= 25:
      signal.append(['buy', time_values[i+1]])

  return signal

def great_stochastic_crossover(dataframe, total_bars):
  great_stochastic_indicator(dataframe)
  signal = []
  time_values = []
  k_values, d_values = ([] for i in range(2))
  for i in reversed(range(total_bars)):
    k_values.append(dataframe.at[i, 'k_great'])
    d_values.append(dataframe.at[i, 'd_great'])
    time_values.append(dataframe.at[i, 'time'])
  for i in range(len(k_values)-2):
    if k_values[i+2] >= d_values[i+1] and k_values[i+1] <= d_values[i+1] and k_values[i+1] >= 75:
      signal.append(['sell', time_values[i+1]])
    if k_values[i+2] <= d_values[i+1] and k_values[i+1] >= d_values[i+1] and k_values[i+1] <= 25:
      signal.append(['buy', time_values[i+1]])

  return signal


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

def time_zone_sync(total_bars, data_frame):
  time_list = []
  for info in reversed(range(total_bars)):
    time_list.append(data_frame.at[info, 'time'] + (6*60*60))
  return time_list

def bulls_and_bears_power(dataframe, bars):
  exponential_moving_average(dataframe, 100)
  bulls_power, bears_power, high, low, fast_ema = ([] for i in range(5))
  for i in reversed(range(bars)):
    high.append((dataframe.at[i, 'high']))
    low.append((dataframe.at[i, 'low']))
    fast_ema.append(dataframe.at[i, 'Fast_EMA'])
  for i in range(len(high) - 1):
    bulls_power.append(high[i] - fast_ema[i])
    bears_power.append(low[i] - fast_ema[i])

  return bulls_power, bears_power

def stochastic_indicator(dataframe):
    k = 14
    d = 3
    slow = 10
    close = dataframe['close']
    low = dataframe['low'].rolling(k).min()
    high = dataframe['high'].rolling(k).max()
    dataframe['%K_Fast'] = (close - low) * 100 / (high - low)
    dataframe['%K'] = dataframe['%K_Fast'].rolling(slow).mean()
    dataframe['%D'] = dataframe['%K'].rolling(d).mean()
    return dataframe['%K'], dataframe['%D']
  
def great_stochastic_indicator(dataframe):
    k = 200
    d = 30
    slow = 5
    close = dataframe['close']
    low = dataframe['low'].rolling(k).min()
    high = dataframe['high'].rolling(k).max()
    dataframe['great_k'] = (close - low) * 100 / (high - low)
    dataframe['k_great'] = dataframe['great_k'].rolling(slow).mean()
    dataframe['d_great'] = dataframe['k_great'].rolling(d).mean()
    return dataframe['k_great'], dataframe['d_great']

def array_moving_average(period, array):
  # Convert array of integers to pandas series
  numbers_series = pd.Series(array)
  # Get the window of series
  # of observations of specified window size
  windows = numbers_series.rolling(period)
  # Create a series of moving
  # averages of each window
  moving_averages = windows.mean()
  # Convert pandas series back to list
  moving_averages_list = moving_averages.tolist()
  # Remove null entries from the list
  final_list = moving_averages_list[period - 1:]

  return final_list

def exponential_moving_average(dataframe, fast=21, slow=100):
    dataframe['Fast_EMA'] = dataframe['close'].ewm(span=fast, adjust=False).mean()
    dataframe['Slow_EMA'] = dataframe['close'].ewm(span=slow, adjust=False).mean()
    return dataframe['Fast_EMA'], dataframe['Slow_EMA']

def is_support(dataframe,i):  
  cond1 = dataframe['low'][i] < dataframe['low'][i-1]   
  cond2 = dataframe['low'][i] < dataframe['low'][i+1]   
  cond3 = dataframe['low'][i+1] < dataframe['low'][i+2]   
  cond4 = dataframe['low'][i-1] < dataframe['low'][i-2]  
  return (cond1 and cond2 and cond3 and cond4) 

# determine bearish fractal
def is_resistance(dataframe,i):  
  cond1 = dataframe['high'][i] > dataframe['high'][i-1]   
  cond2 = dataframe['high'][i] > dataframe['high'][i+1]   
  cond3 = dataframe['high'][i+1] > dataframe['high'][i+2]   
  cond4 = dataframe['high'][i-1] > dataframe['high'][i-2]  
  return (cond1 and cond2 and cond3 and cond4)

# to make sure the new level area does not exist already
def is_far_from_level(value, levels, dataframe, tuner):
  # tuner = 0.001 # 1 Minute : 0.001, 1 Hour : 0.004
  ave =  np.mean((dataframe['high'] - dataframe['low'])) + tuner
  return np.sum([abs(value-level)<ave for _,level in levels])==0

# Store Horizontal level information
def store_levels(data_frame, tuner):
  level = []
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
  return level

# For human visualization
def plotter(levels, dataframe):    
  fig, ax = plt.subplots(figsize=(150, 60))
  candlestick_ohlc(ax,dataframe.values,width=30, colorup='green', 
    colordown='red', alpha=1)
  for level in levels:
    plt.hlines(level[1], xmin = dataframe['time'][level[0]], xmax = 
      max(dataframe['time']), colors='blue', linestyle='-')
  fig.show()

def horizontal_line_values(hline_value_list):
  hline_output_values = []
# Return values of levels in list format
  for i in range(len(hline_value_list)):
    value = hline_value_list[i] # [(13, 1.00002)]
    line_values = list(value) # [13, 1.00002]
    hline_output_values.append(line_values)
  return hline_output_values

def horizontal_line_position(total_bars, hline_output, data_frame, hline_position):
    bar_position = data_frame.at[total_bars - 1, 'close']
    differnece = []
    above, below = 1, -1
    for i in range(len(hline_output)):
        diff = abs(bar_position - hline_output[i][1])
        differnece.append(diff)
        hline_position.append([diff, hline_output[i][1]])

    differnece = min(differnece)
    x = [x for x in hline_position if differnece in x][0]
    position = hline_position.index(x)
    hline_position = hline_position[position][1]
    if bar_position - hline_position > 0:
        return hline_position, above, bar_position
    else:
        return hline_position, below, bar_position

########################################
#
# Laguerre RSI
#
def ehlers_RSI(dataframe, gamma=0.75, smooth=1, debug=bool):
    """
    Laguerra RSI
    How to trade lrsi:  (TL, DR) buy on the flat 0, sell on the drop from top,
    not when touch the top
    """

    df = dataframe
    g = gamma
    smooth = smooth
    debug = debug
    if debug:
        from pandas import set_option
        set_option('display.max_rows', 2000)
        set_option('display.max_columns', 8)

    """
    Vectorised pandas or numpy calculations are not used
    in Laguerre as L0 is self referencing.
    Therefore we use an intertuples loop as next best option.
    """
    lrsi_l = []
    L0, L1, L2, L3 = 0.0, 0.0, 0.0, 0.0
    for row in df.itertuples(index=True, name='lrsi'):
        """ Original Pine Logic  Block1
        p = close
        L0 = ((1 - g)*p)+(g*nz(L0[1]))
        L1 = (-g*L0)+nz(L0[1])+(g*nz(L1[1]))
        L2 = (-g*L1)+nz(L1[1])+(g*nz(L2[1]))
        L3 = (-g*L2)+nz(L2[1])+(g*nz(L3[1]))
        """
        # Feed back loop
        L0_1, L1_1, L2_1, L3_1 = L0, L1, L2, L3

        L0 = (1 - g) * row.close + g * L0_1
        L1 = -g * L0 + L0_1 + g * L1_1
        L2 = -g * L1 + L1_1 + g * L2_1
        L3 = -g * L2 + L2_1 + g * L3_1

        """ Original Pinescript Block 2
        cu=(L0 > L1? L0 - L1: 0) + (L1 > L2? L1 - L2: 0) + (L2 > L3? L2 - L3: 0)
        cd=(L0 < L1? L1 - L0: 0) + (L1 < L2? L2 - L1: 0) + (L2 < L3? L3 - L2: 0)
        """
        cu = 0.0
        cd = 0.0
        if (L0 >= L1):
            cu = L0 - L1
        else:
            cd = L1 - L0

        if (L1 >= L2):
            cu = cu + L1 - L2
        else:
            cd = cd + L2 - L1

        if (L2 >= L3):
            cu = cu + L2 - L3
        else:
            cd = cd + L3 - L2

        """Original Pinescript  Block 3
        lrsi=ema((cu+cd==0? -1: cu+cd)==-1? 0: (cu/(cu+cd==0? -1: cu+cd)), smooth)
        """
        if (cu + cd) != 0:
            lrsi_l.append(cu / (cu + cd))
        else:
            lrsi_l.append(0)

    return lrsi_l
