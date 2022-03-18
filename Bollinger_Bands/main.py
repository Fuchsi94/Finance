from email.policy import default
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('-t', '--ticker', help='input the ticker symbol', default='aapl')
parser.add_argument('-d', '--date', help='input the start date of analysis', default='2021-01-01')
args = parser.parse_args()


df = yf.download(args.ticker, start=args.date)

#simple moving average
df['SMA'] = df.Close.rolling(window=20).mean()

#standard deviation
df['STDDEV'] = df.Close.rolling(window=20).std()

#upper band
df['UPPER'] = df.SMA + 2 * df.STDDEV

#lower band
df['LOWER'] = df.SMA - 2 * df.STDDEV

#buy signal
df['BUY'] = np.where(df.LOWER > df.Close, True, False)

#sell signal
df['SELL'] = np.where(df.UPPER < df.Close, True, False)

#delete NAN
df = df.dropna()

buys = []
sells = []

for i in range(len(df)):
    if df.BUY[i] == True:
        buys.append(i)
    elif df.SELL[i] == True:
        sells.append(i)

#plot
parameters = ['Close', 'SMA', 'UPPER', 'LOWER']
plt.figure(figsize=(12,6))
plt.plot(df[parameters])
plt.scatter(df.index[df.BUY], df[df.BUY].Close, marker = '^', color = 'g')
plt.scatter(df.index[df.SELL], df[df.SELL].Close, marker = 'v', color = 'r')
plt.fill_between(df.index, df.UPPER, df.LOWER, color='grey', alpha=0.3)
plt.legend(parameters)
plt.title(args.ticker)
plt.show()