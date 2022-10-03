
import MetaTrader5 as meta
from time import sleep
from Functions import great_stochastic_crossover, price_data_frame, speaker,\
                    stochastic_crossover, stochastic_indicator,\
                    exponential_moving_average, time_converter,\
                    williams_r_crossover

while True:
    total_bars = 1000 # Use larger values for great stochastic indicator
    symbol = 'EURUSD'
    df = price_data_frame(symbol, meta.TIMEFRAME_M1, total_bars)

    wpr_signal = williams_r_crossover(df, total_bars)
    stoch_signal = stochastic_crossover(df, total_bars)
    great_stoch_signal = great_stochastic_crossover(df, total_bars)
    secondary_time_difference = int(abs(wpr_signal[0][1] - stoch_signal[0][1]) / 60)
    primary_time_difference  = int(abs(stoch_signal[0][1] - great_stoch_signal[0][1]) / 60)

    if wpr_signal[0][0] == 'buy' and stoch_signal[0][0] == 'buy' and secondary_time_difference<=12:
        if stoch_signal[0][0] == 'buy' and great_stoch_signal[0][0] == 'buy' and primary_time_difference <= 20:
            print('BUY   : {0}'.format(time_converter(stoch_signal[0][1])))
            if secondary_time_difference <= 5:
                speaker('Buy', 10)
    if wpr_signal[0][0] == 'sell' and stoch_signal[0][0] == 'sell' and secondary_time_difference<=12:
        if stoch_signal[0][0] == 'sell'  and great_stoch_signal[0][0] == 'sell' and primary_time_difference <= 20:
            print('SELL  : {0}'.format(time_converter(stoch_signal[0][1])))
            if secondary_time_difference <= 5:
                speaker('Sell', 10)

    print('=======================================')
    print("William's Percentage      : ",wpr_signal[0][0])
    print("Stochastic                : ",stoch_signal[0][0])
    print('Great Stochastic          : ', great_stoch_signal[0][0])
    print('Normal Signal difference  : ',secondary_time_difference,'minutes')
    print('Great Signal difference   : ',primary_time_difference,'minutes')
    print('=======================================')
    sleep(30)
    