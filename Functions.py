import MetaTrader5 as meta
from math import floor
import pandas as pd
from mplfinance.original_flavor import candlestick_ohlc
import numpy as np
import matplotlib.pyplot as plt
import time
from pygame import mixer
from ta.momentum import williams_r
from datetime import datetime

def initialization_check():
    if not meta.initialize():
        print('Initialization failed.\nError code : ', meta.last_error())
        quit()

def buy_sell_signal(dataframe, period, total_bars):
  times = [19, 20, 21, 22, 23]
  if time_detector(dataframe, total_bars) not in times:
    stochastic_indicator(dataframe, 21, 5, 7)
    k_line = []  # Fast Line
    d_line = []  # Slow Line
    time_now = []
    close_pos = []
    for info in reversed(range(0,total_bars - 2)):
        k_line.append(dataframe.at[info, '%K'])
        d_line.append(dataframe.at[info, '%D'])
        time_now.append(dataframe.at[info, 'time'])
        close_pos.append(dataframe.at[info, 'close'])
    for i in range(total_bars-2):
      if k_line[i + 2] < d_line[i + 2] and k_line[i+1] > d_line[i+1] and \
        (d_line[i+1] <= 25 or k_line[i+1] <= 25):
        if trix(period, dataframe)[0] > trix(period, dataframe)[1] > trix(period, dataframe)[2] and \
          trix(period, dataframe)[0] > 0 and trix(period, dataframe)[2] < trix(period, dataframe)[1] < 0:
          return 'BUY'
      if k_line[i + 2] > d_line[i + 2] and k_line[i+1] < d_line[i+1] and \
        (d_line[i+1] >= 75 or k_line[i+1] <= 75):
        if trix(period, dataframe)[0] < trix(period, dataframe)[1] < trix(period, dataframe)[2] and \
          trix(period, dataframe)[0] < 0 and trix(period, dataframe)[2] > trix(period, dataframe)[1] > 0:
          return 'SELL'

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

def play_sound(order):
  mixer.init()
  buy_sound = 'buy.mp3'
  sell_sound = 'sell.mp3'
  if order == 'buy':
    mixer.music.load(buy_sound)
  if order == 'sell':
    mixer.music.load(sell_sound)
  mixer.music.play()
  while mixer.music.get_busy():  # wait for music to finish playing
    time.sleep(1)

def trix(period, dataframe):
    dataframe['EMA_1'] = dataframe['close'].ewm(span=period, adjust=False).mean()
    dataframe['EMA_2'] = dataframe['EMA_1'].ewm(span=period, adjust=False).mean()
    dataframe['EMA_3'] = dataframe['EMA_2'].ewm(span=period, adjust=False).mean()
    # TRIX = ( EMA3 [today] - EMA3 [yesterday] ) / EMA3 [yesterday]
    return dataframe['EMA_3']

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
    if williams_r_list[i+1] >= -10:
      signal.append(['sell', time_values[i+1]])
    if williams_r_list[i+1] <= -90:
      signal.append(['buy', time_values[i+1]])

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
    if k_values[i+2] >= d_values[i+1] and k_values[i+1] <= d_values[i+1] and k_values[i+1] >= 70:
      signal.append(['sell', time_values[i+1]])
    if k_values[i+2] <= d_values[i+1] and k_values[i+1] >= d_values[i+1] and k_values[i+1] <= 30:
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
    # axis = dataframe[['%K', '%D']].plot()
    # axis.axhline(20, linestyle='--', color="r")
    # axis.axhline(80, linestyle="--", color="r")
    # plt.show()
    return dataframe['%K'], dataframe['%D']


def exponential_moving_average(dataframe, fast=21, slow=100):
    dataframe['Fast_EMA'] = dataframe['close'].ewm(span=fast, adjust=False).mean()
    dataframe['Slow_EMA'] = dataframe['close'].ewm(span=slow, adjust=False).mean()
    return dataframe['Fast_EMA'], dataframe['Slow_EMA']

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

def horizontal_line_values(hline_values):
  hline_output_values = []
# Return values of levels in list format
  for i in range(len(hline_values)):
    value = hline_values[i] # [(13, 1.00002)]
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