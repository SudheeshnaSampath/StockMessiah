# Team Members:

# Kirtiman Rai |  kirtimar@andrew.cmu.edu

# Mihir Rao | msrao@andrew.cmu.edu

# Soumya Ruraraju | srudrara@andrew.cmu.edu

# Sudheeshna Sampath | sudheess@andrew.cmu.edu

#### Beware: This file runs for 15 mins as it scrapes the data for all 91 stocks together and writes into yahoo_finance.csv

#Description: This module is the goto module for any webscraping requirement.Run this code to get yahoo_finance.csv file
#that powers our Stock Screener feature (previous webscraped data)






#live web scrapping of stock details from yahoo finance web page

import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import urllib.request as ur
import requests
from datetime import datetime


def getCompanyFromSymbol(symbol):
    
    mkp=pd.read_csv('Market_Screener_FInal_File.csv')
    val=mkp[mkp['Symbol']==symbol]['Company'].values[0]
    return val

def getSymbolFromCompany(Company):
    
    mkp=pd.read_csv('Market_Screener_FInal_File.csv')
    val=mkp[mkp['Company']==Company]['Symbol'].values[0]
    return val

####Price####
def get_price(stock):
    index=stock
    url_stats = "https://finance.yahoo.com/quote/" + index +"/key-statistics?p="+ index
    url_stats
    req = ur.Request(url_stats, headers={'User-Agent': 'Mozilla/5.0'})  
    read_data = ur.urlopen(req).read() 
    soup_is= BeautifulSoup(read_data,"lxml")
    ls= [] # Create empty list

    for l in soup_is.find_all('span',{'class':"Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)"}): 
         ls.append(l.string)
     
    price1=float(ls[0].replace(",",""))
    return price1

###Final dataframe
def get_variables(stock):
    index=stock
    url_stats = "https://finance.yahoo.com/quote/" + index +"/key-statistics?p="+ index
    url_stats
    req = ur.Request(url_stats, headers={'User-Agent': 'Mozilla/5.0'})  
    read_data = ur.urlopen(req).read() 
    soup_is= BeautifulSoup(read_data,"lxml")
    ls= [] # Create empty list

##Read all the relevant elements of the table and store it ls
    for l in soup_is.find_all(['span','td']): 
         ls.append(l.string)
    ls 
    ls=ls[14:]
    ls=ls[:len(ls)-11]
    ls = [e for e in ls if e not in ( 'Valuation Measures','Balance Sheet', 'Dividends & Splits', 'Management Effectiveness', 'Share Statistics'
                                    'Financial Highlights','Income Statement','Profitability','Cash Flow Statement','Financial Highlights','Trading Information',
     'Stock Price History','Fiscal Year',
     'Fiscal Year Ends',
     'Mar 31, 2019',
     'Most Recent Quarter',

     'Dec 31, 2019','Share Statistics')]# Exclude those columns
    ls=list(filter(None,ls))
    ls
    #index=[8,11,20,45,48,51,54,57,60,63,74,79,92,95,106,121,124,129]
    index_ls = []
    num = len(ls)
    i = 0

##Remove NAs
    while i < num-1:
        if ls[i] == ls[i+1] and ls[i] == 'N/A':
            index_ls.append(ls[i])
            i += 2
        else:
            index_ls.append(ls[i])
            i = i + 1
    new_ls=index_ls
    new_ls
    stat_data = list(zip(*[iter(new_ls)]*2))
    stat_data
    global stat_st
    stat_st = pd.DataFrame(stat_data[0:])
    stat_st = stat_st.T # Transpose Dataframe
    stat_st.columns = stat_st.iloc[0] #Name columns to first row of dataframe
    stat_st.drop(stat_st.index[0],inplace=True) #Drop first index row
    stat_st
    stat_st.index.name = "" # Remove the index name
    stat_st=stat_st.replace(to_replace="N/A",value=float(0.0))
    stat_st.head()
    ls[ls.index('5 Year Average Dividend Yield')+1]
    stats=pd.DataFrame(['AAPL'],columns=['Stock'])
    stats['Stock']=stock
    stats['Company']=getCompanyFromSymbol(stock)
    
  ##Multiple Try except blocks to tackls NAs
    try:
        ls[ls.index('Market Cap (intraday)')+1]
        try:
            stats['market_cap_in_trillions']=float(str(ls[ls.index('Market Cap (intraday)')+1]).replace('T',''))*10**12
        except:
            if('B' in str(ls[ls.index('Market Cap (intraday)')+1])):
                try:
                    stats['market_cap_in_trillions']=float(str(ls[ls.index('Market Cap (intraday)')+1]).replace('B',''))*10**9
                except:
                    stats['market_cap_in_trillions']=0.0
            elif('M' in str(ls[ls.index('Market Cap (intraday)')+1])):
                try:
                    stats['market_cap_in_trillions']=float(str(ls[ls.index('Market Cap (intraday)')+1]).replace('M',''))*10**6
                except:
                    stats['market_cap_in_trillions']=0.0
            else:
                stats['market_cap_in_trillions']=0.0
    except:
           stats['market_cap_in_trillions']=0.0
        
    try:
        stats['dividend_yield_in_perc']=float(ls[ls.index('5 Year Average Dividend Yield')+1])
        
    except:
         stats['dividend_yield_in_perc']=0.00
            
    try:
        stats['PEG_ratio']=float(ls[ls.index('PEG Ratio (5 yr expected)')+1])   
    except:
        stats['PEG_ratio']=0.00
    
    try:
        stats['Trailing P/E']=float(ls[ls.index('Trailing P/E')+1])   
    except:
        stats['Trailing P/E']=0.00   
    try:
        stats['Beta']=float(ls[ls.index('Beta (5Y Monthly)')+1])   
    except:
        stats['Beta']=0.00  
        
    try:
        stats['Book Value Per Share']=float(ls[ls.index('Book Value Per Share')+1])   
    except:
        stats['Book Value Per Share']=0.00     

    try:
        stats['Dividend Yield TTM']=float(ls[ls.index('Trailing Annual Dividend Yield')+1])   
    except:
        stats['Dividend Yield TTM']=0.00         
    stats['price']=get_price(stock)
    return stats

    
##Scrape for previous downlaoded data
if __name__ =='__main__':
    
    global stock
    global final_stats
    global price
    global url_stats
    final_stats=pd.DataFrame()# Final dataframe to store scraping data for all stocks
    stock='AMZN'#Default value
    stock
        
    
    
    #Read Market Screener to get unique list of symbols
    mkp=pd.read_csv('Market_Screener_FInal_File.csv')
    
    
    ls1=[]
    
    #Store all symbols in list
    ls1=mkp['Symbol'].unique()
    
    #Remove nans if any
    ls1=[x for x in ls1 if str(x) != 'nan']
    
#Loop though every symbol and scrape it's data.     
    for i in range(len(ls1)):
        price=get_price(ls1[i])
        final_df=get_variables(ls1[i])
        final_stats=pd.concat([final_stats,final_df],axis=0,ignore_index=True)
        final_stats   
        
    final_stats.to_csv("yahoo_finance_file_"+str(datetime.now())+'.csv',index=False)
    
