import MetaTrader5 as meta
from math import floor, ceil
import pandas as pd
from mplfinance.original_flavor import candlestick_ohlc
import numpy as np
import matplotlib.pyplot as plt
from pandas_ta import rsi, stoch
from ta.trend import trix as tr
from ta.trend import macd, macd_signal
from ta.utils import _sma
from datetime import datetime
import win32com.client
import numpy as np
import time as current_unix_time

def speaker(message, repeat):
  speaker = win32com.client.Dispatch("SAPI.SpVoice")
  for i in range(repeat):
    speaker.Speak(message)

def initialization_check():
    if not meta.initialize():
        print('Initialization failed.\nError code : ', meta.last_error())
        quit()

def macd_crossover(close, time):
  macd_line = macd(close, 8, 5).tolist()
  macd_signal_line = macd_signal(close, 8, 5, 3).tolist()
  time = time.tolist()
  macd_line.reverse()
  macd_signal_line.reverse()
  time.reverse()
  signal = []
  for i in range(len(macd_line) - 2):
    if macd_line[i+2] < macd_signal_line[i+2] and macd_line[i+1] > macd_signal_line[i+1]:
      signal.append(['buy', time[i]])
    if macd_line[i+2] > macd_signal_line[i+2] and macd_line[i+1] < macd_signal_line[i+1]:
      signal.append(['sell', time[i]])
  return signal

def trend_detect(close, time):
  rsi_line = rsi(close, 14)
  rsi_ma_line = _sma(rsi_line, 14).tolist()
  rsi_line = rsi_line.tolist()
  time = time.tolist()
  rsi_line.reverse()
  rsi_ma_line.reverse()
  time.reverse()
  status = []
  for i in range(len(rsi_ma_line)-2):
    if rsi_ma_line[i+1] < 50 and rsi_ma_line[i+2] < 50:
      status.append(['down_trend', time[i]])
    if rsi_ma_line[i+1] > 50 and rsi_ma_line[i+2] > 50:
      status.append(['up_trend', time[i]])
    
  return status

def macd_signal_detect(close, time):
  macd_line = macd(close, 8, 5).tolist()
  macd_signal_line = macd_signal(close, 8, 5, 3).tolist()
  time = time.tolist()
  time.reverse()
  macd_line.reverse()
  macd_signal_line.reverse()
  status = []
  for i in range(len(macd_signal_line)-2):
    if macd_signal_line[i+2] < 0 and macd_signal_line[i+1] > 0:
      status.append(['buy', time[i]])
    if macd_signal_line[i+2] > 0 and macd_signal_line[i+1] < 0:
      status.append(['sell', time[i]])
  return status

def printer_function(trend_detection, macd_detect, print_message, speak_message):
  time_difference = abs(((current_unix_time.time() - (macd_detect[0][1]))) / 60)
  if trend_detection[0][0] == 'up_trend' and macd_detect[0][0] == 'buy' and time_difference <= 2:
        print(f'{print_message} --> UP  , TIME: {time_converter(macd_detect[0][1])}')
        speaker(f'{speak_message} UP', 10)
  if trend_detection[0][0] == 'down_trend' and macd_detect[0][0] == 'sell' and time_difference <= 2:
        print(f'{print_message} --> DOWN, TIME: {time_converter(macd_detect[0][1])}')
        speaker(f'{speak_message} DOWN', 10)

def line_graph_crossover(close, time):
  line_graph_sma = _sma(close, 14).tolist()
  line_graph = close.tolist()
  time = time.tolist()
  line_graph.reverse()
  time.reverse()
  line_graph_sma.reverse()
  signal = []
  for i in range(len(line_graph_sma)-2):
    if line_graph[i+2] > line_graph_sma[i+2] and line_graph[i+1] < line_graph_sma[i+1]:
      signal.append(['sell', time[i]])
    if line_graph[i+2] < line_graph_sma[i+2] and line_graph[i+1] > line_graph_sma[i+1]:
      signal.append(['buy', time[i]])
    
  return signal  


def time_detector(dataframe, bars):
    std_time = 1661968800 + 6*60*60
    current_time = []
    for i in reversed(range(bars)):
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

def rsi_peaks(close, time):
  RSI = rsi(close, 14).tolist()
  time = time.tolist()
  RSI.reverse()
  time.reverse()
  peaks = []
  for i in range(len(RSI) - 4):
    if RSI[i] != 'nan':
        # RSI Peak
        if RSI[i] < RSI[i+1] and RSI[i+1] > RSI[i+2]:
            # if abs(RSI[i+2] - RSI[i]) >= 2.5 and abs(RSI[i+2] - RSI[i+4])>= 2.5:
                peaks.append([RSI[i+1], time[i+1]])

  return peaks

def rsi_bottoms(close, time):
  RSI = rsi(close, 14).tolist()
  time = time.tolist()
  RSI.reverse()
  time.reverse()
  peaks = []
  for i in range(len(RSI) - 4):
    if RSI[i] != 'nan':
        # RSI Peak
        if RSI[i] > RSI[i+1] and RSI[i+1] < RSI[i+2]:
            # if abs(RSI[i+2] - RSI[i]) >= 2.5 and abs(RSI[i+2] - RSI[i+4])>= 2.5:
                peaks.append([RSI[i+1], time[i+1]])

  return peaks

def rsi_crossover(close, time):
  rsi_list = rsi(close, 14)
  signal, time_values = ([] for i in range(2))
  time_values = time.tolist()
  time_values.reverse()
  rsi_ma_list = _sma(rsi_list, 14).tolist()
  rsi_list = rsi_list.tolist()
  rsi_list.reverse()
  rsi_ma_list.reverse()
  for i in range(len(rsi_ma_list) - 2):
    if rsi_list[i+2] < rsi_ma_list[i+2] and rsi_list[i+1] > rsi_ma_list[i+1]:
      signal.append(['buy', time_values[i]])
    if rsi_list[i+2] > rsi_ma_list[i+2] and rsi_list[i+1] < rsi_ma_list[i+1]:
      signal.append(['sell', time_values[i]])
  return signal

def stochastic_crossover(high, low, close, time):
  stoch_list = stoch(high, low, close, 8, 3, 5)
  k_values, d_values, time_values, signal = ([] for i in range(4))
  k_values = stoch_list['STOCHk_8_3_5'].tolist()
  d_values = stoch_list['STOCHd_8_3_5'].tolist()
  time_values = time.tolist()
  k_values.reverse()
  d_values.reverse()
  time_values.reverse()
  for i in range(len(k_values)-2):
    if k_values[i+2] >= d_values[i+2] and k_values[i+1] <= d_values[i+1]:
      signal.append(['sell', time_values[i]])
      # signal.append('SELL')
    if k_values[i+2] <= d_values[i+2] and k_values[i+1] >= d_values[i+1]:
      signal.append(['buy', time_values[i]])
      # signal.append('BUY')

  return signal

def price_data_frame(symbol, time_frame, bars):
    initialization_check()
    # Retrieving previous bar positions (Open, High, Low, Close, Tick Volume)
    price_rates = meta.copy_rates_from_pos(symbol, time_frame, 0, bars)
    meta.shutdown()
    # Converting into an easy-to-read pandas data frame
    data_frame = pd.DataFrame(price_rates)
    # Converting time
    # data_frame['time'] = pd.to_datetime(data_frame['time'], unit='s')
    return data_frame

def time_zone_sync(bars, data_frame):
  time_list = []
  for info in reversed(range(bars)):
    time_list.append(data_frame.at[info, 'time'] + (6*60*60))
  return time_list

# Below stochastic indicator should be used with 20 EMA
def stochastic_indicator(dataframe, k = 8, d = 3, slow = 5):
    close = dataframe['close']
    low = dataframe['low'].rolling(k).min()
    high = dataframe['high'].rolling(k).max()
    dataframe['%K_Fast'] = (close - low) * 100 / (high - low)
    dataframe['%K'] = dataframe['%K_Fast'].rolling(slow).mean()
    dataframe['%D'] = dataframe['%K'].rolling(d).mean()

def list_ema(data_list, period):
  i = 0
  ema_of_list = []
  while i < len(data_list) - period + 1:
    values = data_list[i : i + period]

    average = sum(values) / period
    ema_of_list.append(average)
    i += 1
  for i in range(period):
    ema_of_list.insert(i, 0)

  return ema_of_list

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
  for i in range(period - 1):
    final_list.insert(i, 0)

  return final_list

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

def horizontal_line_position(bars, hline_output, data_frame, hline_position):
    bar_position = data_frame.at[bars - 1, 'close']
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
