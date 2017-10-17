import datetime as dt
from pandas_datareader import data, wb

start_date = dt.datetime(1995, 1, 1)
dat = data.DataReader('USDBRL=X', 'yahoo')['Adj Close']
dat.to_csv('eurusd.csv', mode='w', header=True)
