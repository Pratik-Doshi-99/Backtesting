import os
import numpy as np
import pandas as pd
from rsi import RSI
from ema import EMA
import datetime as dt

samples = os.listdir(r'Z:\School\Sem 4\Research Methodology\Paper\Sample')  

'''
samples is a list of the csv files that contain the historical prices of the stocks taken as sample
'''

#RSI 14 Days

start_date = dt.datetime(2010,4,1,0)- dt.timedelta(days = 13)
end_date = dt.datetime(2019,3,31,0)
summaries = []

for s in samples:
    df = pd.read_csv(r'Z:\School\Sem 4\Research Methodology\Paper\Sample\\' + s)
    df['Date'] = pd.to_datetime(df['Date'])
    df = df[df['Date'] >= start_date]
    df = df[df['Date'] <= end_date]
    rsi_obj = RSI(column = 'Close',u_level = 60,l_level = 40)
    rsi_obj.generate(df,calc_returns = True)
    summ = rsi_obj.get_summary()
    summaries.append(np.hstack(([[s[:-7]] for _ in range(summ.shape[0])],summ)))


summ = summaries[0]
for i,s in enumerate(summaries):
    if i == 0:
        continue
    summ = np.vstack((summ,s))

rsi_returns = pd.DataFrame(summ, columns = ['Security','Return','Holding Period','Purchase Date'])
rsi_returns.to_csv(r'Z:\School\Sem 4\Research Methodology\Paper\RSI_Returns.csv', index = False)



#EMA (suited for 13-34 days. For other periods, change the period_1 and period_2 attribute while creating EMA object.

for s in samples:
    df = pd.read_csv(r'Z:\School\Sem 4\Research Methodology\Paper\Sample\\' + s)
    df['Date'] = pd.to_datetime(df['Date'])
    df = df[df['Date'] >= start_date]
    df = df[df['Date'] <= end_date]
    ema_obj = EMA(period_1 = 13, period_2 = 34)
    ema_obj.generate(df,calc_returns = True)
    summ = ema_obj.get_summary()
    summaries.append(np.hstack(([[s[:-7]] for _ in range(summ.shape[0])],summ)))

summ = summaries[0]
for i,s in enumerate(summaries):
    if i == 0:
        continue
    summ = np.vstack((summ,s))

ema_returns = pd.DataFrame(summ, columns = ['Security','Return','Holding Period','Purchase Date'])
ema_returns.to_csv(r'Z:\School\Sem 4\Research Methodology\Paper\EMA_13_34_Returns.csv', index = False)
