# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 17:00:10 2020

@author: ijurkovic
"""

import sqlite3
import os
import pandas as pd

parent_dir = 'C:\\Users\\ijurkovic\\Desktop\\Trading'
path = 'C:\\Users\\ijurkovic\\Desktop\\Trading\\\Database'

if os.path.exists(path) == False:
    os.mkdir(path)

os.chdir(path)
os.getcwd()


conn = sqlite3.connect('product.sqlite')
cur = conn.cursor()

filenames = ['NASDAQ.txt','NYSE.txt']

cur.executescript('''create table listedShare (ticker text unique
                                    , companyName text
                                    , industryID integer
                                    , sectorID integer
                                    , countryID integer
                                    , exchangeID integer
                                    , marketCap numeric
                                    , primary key (ticker,companyName));
                    create table delistedShare (ticker text unique
                                    , companyName text
                                    , industryID integer
                                    , sectorID integer
                                    , countryID integer
                                    , exchangeID integer
                                    , marketCap numeric
                                    , date text
                                    , primary key (ticker,companyName));
                    create table listedShareStage (ticker text unique
                                    , companyName text)
                    ''')


####Load new stocks into a table, add remove the delisted ones to a delisted table
tickers = pd.DataFrame() 
for file in filenames:
    file = parent_dir + '\\' + file
    data = pd.read_csv(file, sep = '\t')
    tickers = tickers.append(data, ignore_index = True)
  

for row in tickers.itertuples():
    sym = row.Symbol
    desc = row.Description
    
    cur.execute('select ticker from listedShareStage where ticker=?',(sym,))
    row = cur.fetchone()
    if row is None:
        cur.execute('insert into listedShareStage (ticker, companyName) values(?, ?)', (sym,desc)) 
    else:
        print(sym, 'was already loaded')
conn.commit()


sql = '''insert into delistedShare
                select l.*, DATE('now') date
                from listedShare l
                    left join listedShareStage ls on l.ticker = ls.ticker
                where ls.ticker is null;
                
                delete from listedShare 
                where ticker in
                    (select l.ticker
                     from listedShare l
                    left join listedShareStage ls on l.ticker = ls.ticker
                    where ls.ticker is null);
                    
                insert into listedShare (ticker, companyName)
                select ls.*
                from listedShareStage ls
                    left join listedShare l on l.ticker = ls.ticker
                where l.ticker is null;
                
                delete from listedShareStage'''

cur.executescript(sql)
conn.commit()

sql = 'select count(*) from listedShare'

for row in cur.execute(sql):
    print(row[0]) 


#sql = '''SELECT name FROM sqlite_master WHERE type='table' ORDER BY name'''
#for row in cur.execute(sql):
#    print(row[0])

cur.close()

