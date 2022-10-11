from time import sleep
from Functions import filter_stochastic_crossover, price_data_frame, stochastic_crossover, time_converter, speaker
import MetaTrader5 as meta

while True:
    bars = 1440
    symbol = 'EURUSD'
    data = price_data_frame(symbol, meta.TIMEFRAME_M1, bars)
    filter_signal = filter_stochastic_crossover(data, bars)
    stoch_signal = stochastic_crossover(data, bars)
    signal_time_difference = int(abs(filter_signal[0][1] - stoch_signal[0][1]) / 60)
    time_difference = int(abs((data.at[1439, 'time']) - stoch_signal[0][1]) / 60)

    if filter_signal[0][0] == 'buy' and stoch_signal[0][0] == 'buy' and signal_time_difference<=4:
        if stoch_signal[0][1] > filter_signal[0][1]:
            print('Long Buy   : {0}'.format(time_converter(stoch_signal[0][1])))
            if time_difference <= 4:
                speaker('Long buy', 10)
        else:
            print('Short Buy   : {0}'.format(time_converter(stoch_signal[0][1])))
            if time_difference <= 4:    
                speaker('Short buy', 5)
    if filter_signal[0][0] == 'sell' and stoch_signal[0][0] == 'sell' and signal_time_difference<=4:
        if stoch_signal[0][1] > filter_signal[0][1]:
            print('Long Sell  : {0}'.format(time_converter(stoch_signal[0][1])))
            if time_difference <= 4:
                speaker('Long sell', 10)    
        else:
            print('Short Sell  : {0}'.format(time_converter(stoch_signal[0][1])))
            if time_difference <= 4:
                speaker('Short sell', 5)

    print('=======================================')
    print("Filter                    : ",filter_signal[0][0])
    print("Stochastic                : ",stoch_signal[0][0])
    print('Signal difference         : ',signal_time_difference,'minutes')
    print('=======================================')
    sleep(30)