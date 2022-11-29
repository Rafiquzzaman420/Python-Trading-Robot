# Almost Perfect until now!

from matplotlib import pyplot as plt
from Functions import price_data_frame, time_converter
import MetaTrader5 as meta
from ta.trend import macd, macd_signal
import numpy as np

bars = 120
gbp_dataframe = price_data_frame('GBPUSDm', meta.TIMEFRAME_M1, bars)
eur_dataframe = price_data_frame('EURUSDm', meta.TIMEFRAME_M1, bars)

gbphigh = gbp_dataframe['high']
gbplow = gbp_dataframe['low']
gbpclose = gbp_dataframe['close']
gbptime = gbp_dataframe['time'].tolist()

eurhigh = eur_dataframe['high']
eurlow = eur_dataframe['low']
eurclose = eur_dataframe['close']
eurtime = eur_dataframe['time'].tolist()

macd_line_gbp = macd(gbpclose, 8, 5).tolist()
macd_line_eur = macd(eurclose, 8, 5).tolist()

macd_signal_line_gbp = macd_signal(gbpclose, 8, 5, 3).tolist()
macd_signal_line_eur = macd_signal(eurclose, 8, 5, 3).tolist()

gbptime.reverse()
eurtime.reverse()
macd_line_gbp.reverse()
macd_line_eur.reverse()
macd_signal_line_gbp.reverse()
macd_signal_line_eur.reverse()

for i in range(len(macd_line_gbp)-2):
    if macd_signal_line_gbp[i+2] > 0 and macd_signal_line_gbp[i+1] < 0:
        print(f'GBP --> SELL : {time_converter(gbptime[i])}')
    if macd_signal_line_gbp[i+2] < 0 and macd_signal_line_gbp[i+1] > 0:
        print(f'GBP --> BUY  : {time_converter(gbptime[i])}')
print('=====================================')
for i in range(len(macd_line_eur)-2):
    if macd_signal_line_eur[i+2] > 0 and macd_signal_line_eur[i+1] < 0:
        print(f'EUR --> SELL : {time_converter(eurtime[i])}')
    if macd_signal_line_eur[i+2] < 0 and macd_signal_line_eur[i+1] > 0:
        print(f'EUR --> BUY  : {time_converter(eurtime[i])}')