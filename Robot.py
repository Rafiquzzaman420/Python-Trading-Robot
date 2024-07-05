
from functions import price_data_frame, time_converter, \
    trend_detect, macd_signal_detect, speaker, printer_function
import MetaTrader5 as meta
from time import sleep

print('==============================================================')
print('================= Robot Started Successfully =================')
print('==============================================================')

while True:
    bars = 200
    gbp_dataframe = price_data_frame('GBPUSDm', meta.TIMEFRAME_M1, bars)
    eur_dataframe = price_data_frame('EURUSDm', meta.TIMEFRAME_M1, bars)
    jpy_dataframe = price_data_frame('USDJPYm', meta.TIMEFRAME_M1, bars)

    gbp_close = gbp_dataframe['close']
    eur_close = eur_dataframe['close']
    jpy_close = jpy_dataframe['close']

    gbp_time = gbp_dataframe['time']
    eur_time = eur_dataframe['time']
    jpy_time = jpy_dataframe['time']

    gbp_trend_detection = trend_detect(gbp_close, gbp_time)
    eur_trend_detection = trend_detect(eur_close, eur_time)
    jpy_trend_detection = trend_detect(jpy_close, jpy_time)

    gbp_macd_signal = macd_signal_detect(gbp_close, gbp_time)
    eur_macd_signal = macd_signal_detect(eur_close, eur_time)
    jpy_macd_signal = macd_signal_detect(jpy_close, jpy_time)

    printer_function(gbp_trend_detection, gbp_macd_signal, 'GBP', 'Pound')
    printer_function(eur_trend_detection, eur_macd_signal, 'EUR', 'EURO')
    printer_function(jpy_trend_detection, jpy_macd_signal, 'JPY', 'Japanese Yen')

    sleep(30)