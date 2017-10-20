#import model.py
#import dbmodel.py
import time
import numpy as np
import plotly as py
import plotly.graph_objs as go
from plotly.graph_objs import *
import pandas_datareader.data as web
from datetime import datetime
from forex_python.converter import CurrencyRates



while True:
    df = web.DataReader('BRL=X', 'yahoo')
    trace = go.Candlestick(x=df.index, open=df.Open, high=df.High, low=df.Low, close=df.Close)
    data = [trace]
    py.offline.plot(data, filename='Updated_historical')
    c = CurrencyRates()
    a =  c.get_rate('USD', 'INR')
    print a
    time.sleep(7200)
