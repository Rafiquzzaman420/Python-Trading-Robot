
import MetaTrader5 as meta
from time import sleep
from Functions import play_sound, price_data_frame,\
                    stochastic_crossover, stochastic_indicator,\
                    exponential_moving_average, time_converter,\
                    williams_r_crossover

while True:
    total_bars = 100
    # When pro account signed in use symbol without m (like --> EURUSD)
    # When standard account signed in use symbol with m (like --> EURUSDm)
    symbol = 'EURUSD'
    df = price_data_frame(symbol, meta.TIMEFRAME_M1, total_bars)
    stochastic_indicator(df)
    exponential_moving_average(df)

    wpr_signal = williams_r_crossover(df, total_bars)
    stoch_signal = stochastic_crossover(df, total_bars)
    time_difference = int(abs(wpr_signal[0][1] - stoch_signal[0][1]) / 60)

    if wpr_signal[0][0] == 'buy' and stoch_signal[0][0] == 'buy' and time_difference<=12:
        print('BUY   : {0}'.format(time_converter(stoch_signal[0][1])))
        if time_difference<=2:
            if stoch_signal[1][0] == 'buy':
                print("Market is currently in 'DOWN-TREND'")
                play_sound('down_trend')
            else:
                play_sound('buy')
    if wpr_signal[0][0] == 'sell' and stoch_signal[0][0] == 'sell' and time_difference<=12:
        print('SELL  : {0}'.format(time_converter(stoch_signal[0][1])))
        if time_difference<=2:
            if stoch_signal[1][0] == 'sell':
                print("Market is currently in 'UP-TREND'")
                play_sound('up_trend')
            else:
                play_sound('sell')

    print('=======================================')
    print("William's Percentage      : ",wpr_signal[0][0])
    print("Stochastic                : ",stoch_signal[0][0])
    print('Signal difference         : ',time_difference,'minutes')
    print('=======================================')
    sleep(30)
    # clear = lambda: os.system('cls')
    # clear()

    