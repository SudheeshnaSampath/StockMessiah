# -*- coding: utf-8 -*-
"""
Created on Sat Oct  9 13:55:11 2021

@author: sudhe
"""
#imported to Stock Messiah to print recommendation based on metric chosen

import pandas as pd

#read data from yahoo finance
df=pd.read_csv('Market_Screener_FInal_File.csv')
yahoo=pd.read_csv('yahoo_finance.csv')
yahoo['PBV Ratio']= yahoo['price']/yahoo['Book Value Per Share']

ls1=df['Symbol'].unique()
ls1=[x for x in ls1 if str(x) != 'nan']
yahoo_final=yahoo.merge(df[['Symbol','Flag','Company']],how='left',left_on='Stock',right_on='Symbol')

#r1 here will vary based on metric dropdown selected
def viewRecco(r1):
    if (r1 in('PEG Ratio','PE Ratio','PBV Ratio')):
        recom1=yahoo_final[yahoo_final[r1]>0].sort_values(r1,ascending=True).head(1)
    elif (r1 in ('5 Year Average Dividend Yield %','Market Capitalization')):
        recom1=yahoo_final.sort_values(r1,ascending=False).head(1)
    elif(r1=='Beta 5Y Monthly'):
        yahoo_final['mod']= abs(abs(yahoo_final[r1])-1)
        recom1=yahoo_final[yahoo_final[r1]>0].sort_values('mod',ascending=True).head(1)
    else:
        recom1=yahoo_final.sort_values(r1,ascending=False).head(1) 
    
    recom1=recom1['Company'].to_string(index=False)
    return recom1
   

   