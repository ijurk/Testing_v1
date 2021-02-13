# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 09:23:35 2020

@author: ijurkovic
"""


#--------------------
#Importing Financial Data
#-------------------

#!pip install pandas-reader
import pandas as pd
pd.core.common.is_list_like = pd.api.types.is_list_like
import pandas_datareader.data as pdr
import datetime as dt
import numpy as np

 


# Download historical data for NIFTY constituent stocks
tickers = ["AAPL","MSFT","CSCO","AMZN","INTC",'IBM','FB']

close_prices = pd.DataFrame() # dataframe to store close price of each ticker
attempt = 0 # initializing passthrough variable
drop = [] # initializing list to store tickers whose close price was successfully extracted
while len(tickers) != 0 and attempt <= 5:
    tickers = [j for j in tickers if j not in drop] # removing stocks whose data has been extracted from the ticker list
    for i in range(len(tickers)):
        try:
            temp = pdr.get_data_yahoo(tickers[i],dt.date.today() - dt.timedelta(3650),dt.date.today())
            temp.dropna(inplace = True)
            close_prices[tickers[i]] = temp["Adj Close"]
            drop.append(tickers[i])       
        except:
            print(tickers[i]," :failed to fetch data...retrying")
            continue
    attempt+=1
    
    
######### getting data using yahoofinancials json format 


from yahoofinancials import YahooFinancials

###for single ticker
ticker = 'AAPL'
yahoo_financials = YahooFinancials(ticker)

historical_stock_prices = yahoo_financials.get_historical_stock_data('2017-09-15', '2018-09-15', 'daily')

###for multiple tickers

all_tickers = ["AAPL","MSFT","CSCO","AMZN","INTC"]

# extracting stock data (historical close price) for the stocks identified
close_prices = pd.DataFrame()
end_date = (dt.date.today()).strftime('%Y-%m-%d')
beg_date = (dt.date.today()-dt.timedelta(365)).strftime('%Y-%m-%d')
cp_tickers = all_tickers
attempt = 0
drop = []
while len(cp_tickers) != 0 and attempt <=5:
    print("-----------------")
    print("attempt number ",attempt)
    print("-----------------")
    cp_tickers = [j for j in cp_tickers if j not in drop]
    for i in range(len(cp_tickers)):
        try:
            yahoo_financials = YahooFinancials(cp_tickers[i])
            json_obj = yahoo_financials.get_historical_stock_data(beg_date,end_date,"daily")
            ohlv = json_obj[cp_tickers[i]]['prices']
            temp = pd.DataFrame(ohlv)[["formatted_date","adjclose"]]
            temp.set_index("formatted_date",inplace=True)
            temp2 = temp[~temp.index.duplicated(keep='first')]
            close_prices[cp_tickers[i]] = temp2["adjclose"]
            drop.append(cp_tickers[i])       
        except:
            print(cp_tickers[i]," :failed to fetch data...retrying")
            continue
    attempt+=1


##### Extracting intraday data
    
### for one ticker 
    
from alpha_vantage.timeseries import TimeSeries

key_path = 'C:\\Users\\ijurkovic\\Desktop\\Udemy - Algo Trading\\AlphaVantageAPIKey.txt'

ts = TimeSeries(key=open(key_path, 'r').read(), output_format = 'pandas')

# Get json object with the intraday data and another with  the call's metadata
data, meta_data = ts.get_intraday(symbol='MSFT',interval='1min', outputsize='full')
  
data = ts.get_intraday(symbol='MSFT',interval='1min', outputsize='full')[0]

data.columns = ['open','high','low','close','volume']


##### Web Scraping

import requests
from bs4 import BeautifulSoup

tickers = ['AAPL','MSFT']
financial_dir = {}

for ticker in tickers:
    temp_dir = {}
    
    #for Balance Sheet

    url = 'https://uk.finance.yahoo.com/quote/' + ticker + '/balance-sheet?p=' + ticker 
    page = requests.get(url)
    page_content = page.content
    soup = BeautifulSoup(page_content, 'html.parser')

    table = soup.find_all('div', {'class' : "M(0) Whs(n) BdEnd Bdc($seperatorColor) D(itb)"})
    
    for t in table:
        rows = t.find_all('div', {'class' : 'rw-expnded'})
        for row in rows:
            temp_dir[row.get_text(separator = '/').split('/')[0]]=row.get_text(separator = '/').split('/')[1]
            
    
     #getting income statement data from yahoo finance for the given ticker
    url = 'https://in.finance.yahoo.com/quote/'+ticker+'/financials?p='+ticker
    page = requests.get(url)
    page_content = page.content
    soup = BeautifulSoup(page_content,'html.parser')
    tabl = soup.find_all("div", {"class" : "M(0) Whs(n) BdEnd Bdc($seperatorColor) D(itb)"})
    for t in tabl:
        rows = t.find_all("div", {"class" : "rw-expnded"})
        for row in rows:
            temp_dir[row.get_text(separator='|').split("|")[0]]=row.get_text(separator='|').split("|")[1]
    
    #getting cashflow statement data from yahoo finance for the given ticker
    url = 'https://in.finance.yahoo.com/quote/'+ticker+'/cash-flow?p='+ticker
    page = requests.get(url)
    page_content = page.content
    soup = BeautifulSoup(page_content,'html.parser')
    tabl = soup.find_all("div", {"class" : "M(0) Whs(n) BdEnd Bdc($seperatorColor) D(itb)"})
    for t in tabl:
        rows = t.find_all("div", {"class" : "rw-expnded"})
        for row in rows:
            temp_dir[row.get_text(separator='|').split("|")[0]]=row.get_text(separator='|').split("|")[1]
    
    #getting key statistics data from yahoo finance for the given ticker
    url = 'https://in.finance.yahoo.com/quote/'+ticker+'/key-statistics?p='+ticker
    page = requests.get(url)
    page_content = page.content
    soup = BeautifulSoup(page_content,'html.parser')
    tabl = soup.findAll("table", {"class": "W(100%) Bdcl(c) "})
    for t in tabl:
        rows = t.find_all("tr")
        for row in rows:
            if len(row.get_text(separator='|').split("|")[0:2])>0:
                temp_dir[row.get_text(separator='|').split("|")[0]]=row.get_text(separator='|').split("|")[-1]    
   
        
   
    financial_dir[ticker] = temp_dir

#storing information in pandas dataframe
combined_financials = pd.DataFrame(financial_dir)
tickers = combined_financials.columns
for ticker in tickers:
    combined_financials = combined_financials[~combined_financials[ticker].str.contains("[a-z]").fillna(False)]

        
  
    

####Basic data handling - NaN values

###replace use the backfill

close_prices.fillna(method = 'backfill',inplace = True)


###Drop NaNs

#close_prices.dropna(axis = 0)

####Mean, Median, Standard deviation, daily return


daily_return = close_prices.pct_change()

##or calculated:

#daily_return = (close_prices/close_prices.shift(1)) - 1

daily_return.mean()
daily_return.median()


##Rolling mean and standard deviation

daily_return.rolling(window = 20).mean()  # simple moving average   min period = 1 would take average of all previous days until it has 20 days at least
daily_return.rolling(window = 20).std()  
daily_return.ewm(span = 20, min_periods = 20).mean() #Exponential moving average
daily_return.ewm(span = 20, min_periods = 20).std()


###Data Visualization

cp_standardized = (close_prices - close_prices.mean())/close_prices.std() #put all prices on same scale

cp_standardized.plot(subplots = True, layout = (3,3), title = "Stock Price Evolution", grid = True)

##PyPlot Demo

import matplotlib.pyplot as plt

fig, ax = plt.subplots()
plt.style.available
plt.style.use('ggplot')
ax.set(title = 'Daily return on stocks', xlabel = 'Stocks', ylabel = 'Daily Return')
plt.bar(daily_return.columns, daily_return.mean())

##### Technical Indicators
###MACD - Moving Average Convergance Divergence

##when MACD cuts signal line from below - bullish period, ; when MACD cuts signal line from above - bearish period

ticker = 'MSFT'

ohlcv = pdr.get_data_yahoo(ticker,dt.date.today()-dt.timedelta(1825),dt.date.today()) 

def MACD(DF, a,b,c):
    df = ohlcv.copy()
    df['MA_fast'] = df['Adj Close'].ewm(span = a, min_periods = a).mean()
    df['MA_slow'] = df['Adj Close'].ewm(span = b, min_periods = b).mean()
    df['MACD'] = df['MA_fast']-df['MA_slow']
    df['Signal'] = df['Adj Close'].ewm(span = c, min_periods = c).mean()
    df.dropna(inplace = True)
    return df


###ADD THE PLOT FROM HIS CODE
    
###Bollinger Bands and ATR (Average True Range)
    
def ATR(DF, n):
    df = DF.copy()
    df['H-L'] = abs(df['High'] - df['Low'])
    df['H-PC'] = abs(df['High'] - df['Adj Close'].shift(1))
    df['L-PC'] = abs(df['Low'] - df['Adj Close'].shift(1))
    df['TR'] = df[['H-L','H-PC','L-PC']].max(axis = 1, skipna = False)
    df['ATR'] = df['TR'].rolling(n).mean()
    df2 = df.drop(['H-L','H-PC','L-PC'],axis = 1)
    df2.dropna(inplace = True)
    return df2
 
    
ATR(ohlcv, 20)

def BollBnd(DF,n):
    df = DF.copy()
    df['MA'] = df['Adj Close'].rolling(n).mean()
    df['BB_up'] = df['MA'] + 2 * df['MA'].rolling(n).std()
    df['BB_dn'] = df['MA'] - 2 * df['MA'].rolling(n).std()
    df['BB_range'] = df['BB_up'] - df['BB_dn']
    df.dropna(inplace = True)
    return df

BollBnd(ohlcv,20).iloc[-100:,[-4,-3,-2]].plot()


###RSI (Relative Strength index)

# value above 70 indicate that the asset has now reached overbought territory
## values below 30 signify oversold territory
## typically 14 days period


def RSI(DF, n):
    df = DF.copy()
    df['delta'] = df['Adj Close'] - df['Adj Close'].shift(1)
    df['gain'] = np.where(df['delta'] > 0 ,df['delta'], 0)
    df['loss'] = np.where(df['delta'] < 0 ,abs(df['delta']), 0)
    avg_gain = []
    avg_loss = []
    gain = df['gain'].tolist()
    loss = df['loss'].tolist()
    for i in range(len(df)):
        if i < n:
            avg_gain.append(np.NaN)
            avg_loss.append(np.NaN)
        elif i == n:
            avg_gain.append(df['gain'].rolling(n).mean().tolist()[n])
            avg_loss.append(df['loss'].rolling(n).mean().tolist()[n])
        elif i > n:
            avg_gain.append(((n-1)*avg_gain[i-1] + gain[i])/n)
            avg_loss.append(((n-1)*avg_loss[i-1] + loss[i])/n)
    df['avg_gain'] = np.array(avg_gain)
    df['avg_loss'] = np.array(avg_loss)
    df['RS'] = df['avg_gain']/df['avg_loss']
    df['RSI'] = 100 - (100/(1 + df['RS']))
    df.dropna(inplace = True)
    return df['RSI']

RSI(ohlcv, 14)
            


#####ADX (Average Directional Index)

## measures strenght of the trend, does not tell direction
## range from 0 - 100
# 0 - 25 - absent or weak trend
# 25 - 50 - strong trend
# 50 - 75 - very strong trend
# 75 - 100 - Extremely strong trend

##typical period 14 


def ADX(DF,n):
    df2 = DF.copy()
    df2['TR'] = ATR(df2,n)['TR']
    df2['DMplus'] = np.where((df2['High'] - df2['High'].shift(1)) > (df2['Low'].shift(1) - df2['Low']),df2['High'] - df2['High'].shift(1),0)
    df2['DMplus'] = np.where(df2['DMplus'] < 0, 0, df2['DMplus'])
    df2['DMminus'] = np.where((df2['Low'].shift(1) - df2['Low']) > (df2['High'] - df2['High'].shift(1)), df2['Low'].shift(1) - df2['Low'], 0)
    df2['DMminus'] = np.where(df2['DMminus'] < 0, 0, df2['DMminus'])
    TRn = []
    DMplusN = []
    DMminusN = []
    TR = df2['TR'].tolist()
    DMplus = df2['DMplus'].tolist()
    DMminus = df2['DMminus'].tolist()
    for i in range(len(df2)):
        if i < n:
            TRn.append(np.NaN)
            DMplusN.append(np.NaN)
            DMminusN.append(np.NaN)
        elif i == n:
            TRn.append(df2['TR'].rolling(n).sum().tolist()[n])      
            DMplusN.append(df2['DMplus'].rolling(n).sum().tolist()[n])     
            DMminusN.append(df2['DMminus'].rolling(n).sum().tolist()[n])
        elif i > n:
            TRn.append(TRn[i - 1] - (TRn[i - 1]/n) + TR[i])
            DMplusN.append(DMplusN[i - 1] - (DMplusN[i - 1]/n) + DMplus[i])
            DMminusN.append(DMminusN[i - 1] - (DMminusN[i - 1]/n) + DMminus[i])
    df2['TRn'] = np.array(TRn)
    df2['DMplusN'] = np.array(DMplusN)
    df2['DMminusN'] = np.array(DMminusN)
    df2['DIplusN'] = 100 * (df2['DMplusN']/df2['TRn'])
    df2['DIminusN'] = 100 * (df2['DMminusN']/df2['TRn'])
    df2['DIsum'] = df2['DMplusN'] + df2['DMminusN']
    df2['DIdiff'] = abs(df2['DMplusN'] - df2['DMminusN'])
    df2['DX'] = 100*(df2['DIdiff']/df2['DIsum'])
    ADX = []
    DX = df2['DX'].tolist()
    for j in range(len(df2)):
        if j < 2*n-1:
            ADX.append(np.NaN)
        elif j == 2*n-1:
            ADX.append(df2['DX'][j-n+1:j+1].mean())
        elif j > 2*n-1:
            ADX.append(((n-1) * ADX[j-1] + DX[j])/n)
    df2['ADX']=np.array(ADX)
    return df2['ADX']
            
            
    
    
ADX(ohlcv,14)


##### OBV On Balance Volume 
## leading indicator
## momentum indicator - based on teh theory that volume proceeds price movement

## OBV raising - price trending upwards
## OBV falling - price trending downwards

def OBV(DF):
    df = DF.copy()
    df['daily_ret'] = df['Adj Close'].pct_change()
    df['direction'] = np.where(df['daily_ret'] >= 0, 1, -1)
    df['direction'][0] = 0
    df['vol_adj'] = df['Volume'] * df['direction']
    df['obv'] = df['vol_adj'].cumsum()
    return df['obv']
    
OBV(ohlcv)


##### Slop implementation

import statsmodels.api as sm

#n - number of how many consecutive points - 5 is a week
#ser - array of adjusted close prices, not teh dataframe

def slope(ser,n):
    slopes = [i*0 for i in range(n-1)]
    for i in range(n,len(ser)+1):
        y = ser[i-n:i]
        x = np.array(range(n))
        y_scaled = (y - y.min())/(y.max() - y.min())
        x_scaled = (x - x.min())/(x.max() - x.min())
        x_scaled = sm.add_constant(x_scaled)
        model = sm.OLS(y_scaled,x_scaled)
        results = model.fit()
        #results.summary() to show the summary of the regressio
        slopes.append(results.params[-1])
    slopes_angle = (np.rad2deg(np.arctan(np.array(slopes))))
    return np.array(slopes_angle)

ser = ohlcv['Adj Close']
n = 5 

df = ohlcv.copy()
df['slope'] = slope(ohlcv['Adj Close'],5)

df.iloc[:,[4,6]].plot(subplots = True, layout = (2,1)) ##plot it


##### Renko Chart

##built using price movements, time scale is not fixed
##new brick is added only when teh price moves by a predetermined amount in either direction

## use this library to do Ranko Link to stocktrend github page - https://github.com/ChillarAnand/stocktrends

from stocktrends import Renko

ATR(ohlcv,120)

def renko_dataframe(DF):
    df = DF.copy()
    df.reset_index(inplace = True)
    df = df.iloc[:,[0,1,2,3,5,6]]
    df.columns = ['date','high','low','open','volume','close']
    renko_df = Renko(df)
    renko_df.brick_size = round(ATR(DF,120)['ATR'][-1],0)
    df2 = renko_df.get_bricks()
    return df2

## True - green brick up trend, False - red brick down trend - look at 3 bricks sa trend indicator


##### TA Lib for Pattern Recognition

import talib
from alpha_vantage.timeseries import TimeSeries
from time import sleep


tickers = ["AAPL","MSFT","CSCO","AMZN","INTC",'IBM','FB']   
key_path = 'C:\\Users\\ijurkovic\\Desktop\\Udemy - Algo Trading\\AlphaVantageAPIKey.txt'
ts = TimeSeries(key=open(key_path, 'r').read(), output_format = 'pandas')


ohlc_tech = {} # dictionary to store close price of each ticker
attempt = 0 # initializing passthrough variable
drop = [] # initializing list to store tickers whose close price was successfully extracted
while len(tickers) != 0 and attempt <= 100:
    tickers = [j for j in tickers if j not in drop] # removing stocks whose data has been extracted from the ticker list
    for i in range(len(tickers)):
        sleep(0.2)
        try:
            ohlc_tech[tickers[i]] = ts.get_daily(symbol=tickers[i], outputsize='full')[0]
            ohlc_tech[tickers[i]].columns = ['Open','High','Low',"Adj Close",'Volume']
            drop.append(tickers[i])       
        except:
            print(tickers[i]," :failed to fetch data...retrying")
            continue
    attempt+=1
    

tickers = ohlc_tech.keys() # redefine tickers variable after removing any tickers with corrupted data
ohlc_dict = ohlc_tech.copy()


for ticker in tickers:
    ohlc_dict[ticker]['3I'] = talib.CDL3INSIDE(ohlc_dict[ticker]['Open']
                                               ,ohlc_dict[ticker]['High']
                                               ,ohlc_dict[ticker]['Low']
                                               ,ohlc_dict[ticker]['Adj Close'])

###FUNDEMENTAL ANALYSIS

##CAGR (compounded annual growth rate) 
##assumes the profits are continously reinvested
 
ticker = '^GSPC'
SnP = temp = pdr.get_data_yahoo(ticker,dt.date.today() - dt.timedelta(1025),dt.date.today())

SnP['Adj Close'].plot()


def CAGR(DF):
    df = DF.copy()
    df['daily_ret'] = df['Adj Close'].pct_change()
    df['cum_return'] = (1 + df['daily_ret']).cumprod()
    n = len(df)/252  ##for daily returns , if you have weekly change to 52 (no of weeks)
    CAGR = (df['cum_return'][-1])**(1/n)-1
    return CAGR

##### Volatility

def volatility(DF):
    df = DF.copy()
    df['daily_ret'] = df['Adj Close'].pct_change()
    vol = df['daily_ret'].std() * np.sqrt(252)
    return vol

##### Sharpe Ratio & Sortino Ratio

def sharpe(DF,rf):
    df = DF.copy()
    sr = (CAGR(df) - rf)/volatility(df)
    return sr

def sortino(DF, rf):
    df = DF.copy()
    df['daily_ret'] = df['Adj Close'].pct_change()
    neg_vol = df[df['daily_ret']<0]['daily_ret'].std() * np.sqrt(252) ## takes only negative returns
    sr = (CAGR(df) - rf)/volatility(df)
    return sr

#### Maximum drawdown and Calmar Ratio


def max_dd(DF):
    df = DF.copy()
    df['daily_ret'] = df['Adj Close'].pct_change()
    df['cum_return'] = (1 + df['daily_ret']).cumprod()
    df['cum_roll_max'] = df['cum_return'].cummax()


