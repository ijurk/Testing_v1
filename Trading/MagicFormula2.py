# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 16:55:16 2020

@author: ijurkovic
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 20:35:51 2020

@author: ijurkovic
"""

import os
import pandas as pd
from datetime import date
import time 
import requests
from bs4 import BeautifulSoup
import sqlite3


today = date.today().strftime('%Y%m%d')

parent_dir = 'C:\\Users\\ijurkovic\\Desktop\\Trading'
path = os.path.join(parent_dir, today)

dbpath = 'C:\\Users\\ijurkovic\\Desktop\\Trading\\\Database'
conn = sqlite3.connect(dbpath + '\\stock_info_db.sqlite')
cur = conn.cursor()

sql = '''select p.ticker
        from Product_Description p 
            left join Industry_Sector i on i.id = p.industry_sector_id
            left join Country c on c.id = p.country_id
        where i.sector not in ('Financial Services') and c.country_code in ('US')'''

tickers_all = []        
for row in cur.execute(sql):
    tickers_all.append(row[0])

if os.path.exists(path) == False:
    os.mkdir(path)

os.chdir(path)
os.getcwd()



def get_fin(tickers):
    financial_dir_cy = {} #directory to store current year's information
    
    starttime = time.time()
    
    for ticker in tickers:
        
        if tickers.index(ticker) != 0 and tickers.index(ticker) % 70 == 0:
            print('We are on ticker number: ', tickers.index(ticker))
            print('Sleeping for 5 min')
            time.sleep(300)
            
        
        try:
            print("scraping financial statement data for ",ticker)
            temp_dir = {}
            
            #Balance Sheet
            
            url = 'https://in.finance.yahoo.com/quote/'+ticker+'/balance-sheet?p='+ticker
            page = requests.get(url)
            page_content = page.content
            soup = BeautifulSoup(page_content,'html.parser')
            tabl = soup.find_all("div", {"class" : "M(0) Whs(n) BdEnd Bdc($seperatorColor) D(itb)"})
            for t in tabl:
                rows = t.find_all("div", {"class" : "rw-expnded"})
                for row in rows:
                    temp_dir[row.get_text(separator='|').split("|")[0]]=row.get_text(separator='|').split("|")[1]
                    
            
            #Income Statement
            url = 'https://uk.finance.yahoo.com/quote/'+ticker+'/financials?p='+ticker
            page = requests.get(url)
            page_content = page.content
            soup = BeautifulSoup(page_content,'html.parser')
            tabl = soup.find_all("div", {"class" : "M(0) Whs(n) BdEnd Bdc($seperatorColor) D(itb)"})
            for t in tabl:
                rows = t.find_all("div", {"class" : "rw-expnded"})
                for row in rows:
                    temp_dir[row.get_text(separator='|').split("|")[0]]=row.get_text(separator='|').split("|")[1]
                
            
            #Cashflow Statement 
            url = 'https://uk.finance.yahoo.com/quote/'+ticker+'/cash-flow?p='+ticker
            page = requests.get(url)
            page_content = page.content
            soup = BeautifulSoup(page_content,'html.parser')
            tabl = soup.find_all("div", {"class" : "M(0) Whs(n) BdEnd Bdc($seperatorColor) D(itb)"})
            for t in tabl:
                rows = t.find_all("div", {"class" : "rw-expnded"})
                for row in rows:
                    temp_dir[row.get_text(separator='|').split("|")[0]]=row.get_text(separator='|').split("|")[1]
                    
                    
            #getting key statistics data from yahoo finance for the given ticker
            url = 'https://uk.finance.yahoo.com/quote/'+ticker+'/key-statistics?p='+ticker
            page = requests.get(url)
            page_content = page.content
            soup = BeautifulSoup(page_content,'html.parser')
            tabl = soup.findAll("table")
            for t in tabl:
                rows = t.find_all("tr")
                for row in rows:
                    if len(row.get_text(separator='|').split("|")[0:2])>0:
                        temp_dir[row.get_text(separator='|').split("|")[0]]=row.get_text(separator='|').split("|")[-1]    
           
            financial_dir_cy[ticker] = temp_dir
            
        except:
            print("Problem scraping data for ",ticker)
    
    endtime = time.time()
    hours, rem = divmod(endtime - starttime, 3600)
    minutes, seconds = divmod(rem, 60)
    print('---Execution time: ' + '{:0>2}:{:0>2}:{:05.2f}'.format(int(hours),int(minutes), seconds))
    return financial_dir_cy

"""
####For testing 
test_dir_cy, test_dir_py, test_dir_py2 = get_fin(tickers)
test_financials_cy = pd.DataFrame(test_dir_cy)
"""

runs_num = 4
round(len(tickers_all) /runs_num,0)
tickers1 = tickers_all[0:int(round(len(tickers_all) /runs_num,0))]
tickers2 = tickers_all[int(round(len(tickers_all) /runs_num,0)):int(round(len(tickers_all) /runs_num,0))*2]
tickers3 = tickers_all[int(round(len(tickers_all) /runs_num,0))*2:int(round(len(tickers_all) /runs_num,0))*3]
tickers4 = tickers_all[int(round(len(tickers_all) /runs_num,0))*3:]



financial_dir_cy = get_fin(tickers1)
print('First round done. Sleeping for 10 min')
time.sleep(600)

runtwo_cy = get_fin(tickers2)
print('Second round done. Sleeping for 10 min')
time.sleep(600)

runthree_cy = get_fin(tickers3)
print('Third round done. Sleeping for 10 min')
time.sleep(600)

runfour_cy = get_fin(tickers4)
print('Fourth round done.')

runone_cy = financial_dir_cy

financial_dir_cy.update(runtwo_cy)

financial_dir_cy.update(runthree_cy)

financial_dir_cy.update(runfour_cy)



#storing information in pandas dataframe
combined_financials_cy = pd.DataFrame(financial_dir_cy)
tickers = combined_financials_cy.columns.tolist() #updating the tickers 

##get list of tickers that were not scrapped 
x = set(tickers_all)
y = set(tickers)
tickers_dropped_web = list(x - y)

##tickers that got Nans
cy_data = combined_financials_cy.T
tickers_nan = cy_data[cy_data['Assets'].isnull()].index.tolist()

##run Nans
runfive_cy = get_fin(tickers_nan)


##get list of tickers dropped
def getList(dict): 
    list = [] 
    for key in dict.keys(): 
        list.append(key) 
          
    return list

tickers = getList(runfive_cy)

x = set(tickers_nan)
y = set(tickers)
tickers_dropped_nan = list(x - y)



##remove the data from initial table based on tickers_nan and add the newly run data 

financial_dir_cy_df = dict(financial_dir_cy)

for ticker in tickers_nan:
    del financial_dir_cy_df[ticker]

financial_dir_cy_df.update(runfive_cy)



combined_financials_cy = pd.DataFrame(financial_dir_cy_df)





def info_filter(df,stats,indx):
    """function to filter relevant financial information for each 
       stock and transforming string inputs to numeric"""
    tickers = df.columns
    all_stats = {}
    for ticker in tickers:
        try:
            temp = df[ticker]
            ticker_stats = []
            for stat in stats:
                ticker_stats.append(temp.loc[stat])
            all_stats['{}'.format(ticker)] = ticker_stats ##format uses the value as a key in the dictionary
        except:
            print("can't read data for ",ticker)
    
    all_stats_df = pd.DataFrame(all_stats,index=indx)
    
    # cleansing of fundamental data imported in dataframe
    all_stats_df[tickers] = all_stats_df[tickers].replace({',': ''}, regex=True)
    all_stats_df[tickers] = all_stats_df[tickers].replace({'M': 'E+03'}, regex=True)
    all_stats_df[tickers] = all_stats_df[tickers].replace({'B': 'E+06'}, regex=True)
    all_stats_df[tickers] = all_stats_df[tickers].replace({'T': 'E+09'}, regex=True)
    all_stats_df[tickers] = all_stats_df[tickers].replace({'%': 'E-02'}, regex=True)
    all_stats_df[tickers] = all_stats_df[tickers].replace({'-$': '0'}, regex=True)
    for ticker in all_stats_df.columns:
        all_stats_df[ticker] = pd.to_numeric(all_stats_df[ticker].values,errors='coerce')
    return all_stats_df

def magic_formula(df, div = True):
    df_copy = df.copy()
    
    if div == False:
        df_copy.drop(index = 'DivYield', inplace = True)
        df_copy.dropna(axis=1,inplace = True)
        tickers = df_copy.columns.tolist()
    else:
        df_copy.dropna(axis=1,inplace = True)
        tickers = df_copy.columns.tolist()
    transpose_df = df_copy.transpose()
    final_stats_df = pd.DataFrame()
    
    
    # calculating relevant financial metrics for each stock
    final_stats_df["EBIT"] = transpose_df["EBITDA"] - transpose_df["D&A"]
    final_stats_df["TEV"] = transpose_df["MarketCap"].fillna(0) \
                            + transpose_df["TotDebt"].fillna(0) \
                            - (transpose_df["CurrAsset"].fillna(0)\
                               - transpose_df["CurrLiab"].fillna(0))
    final_stats_df["EarningYield"] =  final_stats_df["EBIT"]/final_stats_df["TEV"]
    final_stats_df["FCFYield"] = (transpose_df["CashFlowOps"]-transpose_df["Capex"])/transpose_df["MarketCap"]
    final_stats_df["ROC"]  = (transpose_df["EBITDA"] - transpose_df["D&A"])/(transpose_df["PPE"]+transpose_df["CurrAsset"]-transpose_df["CurrLiab"])
    final_stats_df["BookToMkt"] = transpose_df["BookValue"]/transpose_df["MarketCap"]
   
    # finding value stocks based on Magic Formula
    final_stats_val_df = final_stats_df.loc[tickers,:]
    final_stats_val_df["CombRank"] = final_stats_val_df["EarningYield"].rank(ascending=False,na_option='bottom')\
                                +final_stats_val_df["ROC"].rank(ascending=False,na_option='bottom')
    final_stats_val_df["MagicFormulaRank"] = final_stats_val_df["CombRank"].rank(method='first')
    value_stocks = final_stats_val_df.sort_values("MagicFormulaRank").iloc[:,[2,4,7]]
    ##if div is equal to true calculate dividnd yield and find highes yielding dividend stock
    if div == True:
        final_stats_df["DivYield"] = transpose_df["DivYield"]
        # finding highest dividend yield stocks
        high_dividend_stocks = final_stats_df.sort_values("DivYield",ascending=False).iloc[:,6]
        # # Magic Formula & Dividend yield combined
        final_stats_df["CombRank"] = final_stats_df["EarningYield"].rank(ascending=False,method='first') \
                                  +final_stats_df["ROC"].rank(ascending=False,method='first')  \
                                  +final_stats_df["DivYield"].rank(ascending=False,method='first')
        final_stats_df["CombinedRank"] = final_stats_df["CombRank"].rank(method='first')
        value_high_div_stocks = final_stats_df.sort_values("CombinedRank").iloc[:,[2,4,6,8]]
    if div == True:
        return high_dividend_stocks, value_high_div_stocks
    else:
         return value_stocks

### Magic formula

# creating dataframe with relevant financial information for each stock using fundamental data
stats_m = ["EBITDA",
         "Depreciation & amortisation",
         "Market cap (intra-day)",
         "Net income available to common shareholders",
         "Net cash provided by operating activities",
         "Capital expenditure",
         "Total current assets",
         "Total current liabilities",
         "Net property, plant and equipment",
         "Total stockholders' equity",
         "Long-term debt",
         "Forward annual dividend yield"] # change as required



indx_m = ["EBITDA","D&A","MarketCap","NetIncome","CashFlowOps","Capex","CurrAsset",
        "CurrLiab","PPE","BookValue","TotDebt","DivYield"]



stats_d = ["Shares outstanding",
         "Market cap (intra-day)",
         ] 
indx_d = ["SharesOut","MarketCap"]


        
# cleansing of fundamental data -  magic
all_stats_df = info_filter(combined_financials_cy,stats_m,indx_m)
transformed_df_cy = info_filter(combined_financials_cy,stats_p,indx_p)
add_stats_df = info_filter(combined_financials_cy,stats_d,indx_d)

stats = add_stats_df.T
stats["Price"] = stats["MarketCap"] / stats["SharesOut"]
stats_data = stats.reset_index(level = 0).rename(columns = {'index': 'ticker'})
for i in range(len(stats_data)):
    if stats_data.iloc[i,2] < 250000:
        stats_data.at[i,'Cap Category'] = 'micro'
    elif stats_data.iloc[i,2] < 2000000:
        stats_data.at[i,'Cap Category'] = 'small'
    elif stats_data.iloc[i,2] < 10000000:
        stats_data.at[i,'Cap Category'] = 'medium'
    elif stats_data.iloc[i,2] < 200000000:
        stats_data.at[i,'Cap Category'] = 'large'
    elif stats_data.iloc[i,2] >= 200000000:
        stats_data.at[i,'Cap Category'] = 'mega'



value_stocks = magic_formula(all_stats_df, div = False)
value_stocks_div = magic_formula(all_stats_df)

value_data = value_stocks.reset_index(level = 0).rename(columns = {'index': 'ticker'})
value_data = pd.merge(value_data, stats_data, how = 'left', on = 'ticker')


value_stocks_file = 'value_stocks.xlsx'
value_data.to_excel(value_stocks_file, index = False, header = True)

fn = 'DroppedWebTickers.txt'
f = open(fn, 'w')
for ticker in tickers_dropped_web:
    f.write(ticker + '\n')
f.close()

fn = 'DroppedNaNTickers.txt'
f = open(fn, 'w')
for ticker in tickers_dropped_nan:
    f.write(ticker + '\n')
f.close()


file = 'combined_fin_cy.txt'
combined_financials_cy.to_csv(file,sep ='\t', index = False, header = True)
file = 'all_stats_df.txt'
all_stats_df.to_csv(file,sep ='\t', index = False, header = True)

