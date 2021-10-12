#display stock screen from previously web scrapped data based on metric chosen

import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt

#print graph of top 3 companies vs metric chosen
def get_graph(metric_option):
    
    df=pd.read_csv('Market_Screener_FInal_File.csv')
    yahoo=pd.read_csv('yahoo_finance.csv')
    yahoo['PBV Ratio']= yahoo['price']/yahoo['Book Value Per Share']
    yahoo_final=yahoo.merge(df[['Symbol','Flag','Company']],how='left',left_on='Stock',right_on='Symbol')


    if (metric_option in('PEG Ratio','PE Ratio','PBV Ratio')):
        #print("based on "+metric_option+"\n")
        graph=yahoo_final[yahoo_final[metric_option]>0].sort_values(metric_option,ascending=True).head(3)
    elif (metric_option in ('5 Year Average Dividend Yield %','Market Capitalization')):
        #print("based on "+metric_option+"\n")
        graph=yahoo_final.sort_values(metric_option,ascending=False).head(3)
    elif(metric_option=='Beta 5Y Monthly'):
        yahoo_final['mod']= abs(abs(yahoo_final[metric_option])-1)
        graph=yahoo_final[yahoo_final[metric_option]>0].sort_values('mod',ascending=True).head(3)
    else:
        graph=yahoo_final.sort_values(metric_option,ascending=False).head(3) 
    my_colors = ['g','b','r']
    fig, ax = plt.subplots()
    graph.plot(x='Company', y=metric_option,kind='bar',ax=ax,title='Top 3 stocks based on '+metric_option,xlabel='Company',ylabel=metric_option,color=my_colors,legend=False,rot=0)  
    return fig

#print table for all metrics for top 3 companies based on metric chosen 
def get_table(metric_option):
    
    df=pd.read_csv('Market_Screener_FInal_File.csv')
    yahoo=pd.read_csv('yahoo_finance.csv')
    yahoo['PBV Ratio']= yahoo['price']/yahoo['Book Value Per Share']
    yahoo_final=yahoo.merge(df[['Symbol','Flag','Company']],how='left',left_on='Stock',right_on='Symbol')


    if (metric_option in('PEG Ratio','PE Ratio','PBV Ratio')):
        #print("based on "+metric_option+"\n")
        graph=yahoo_final[yahoo_final[metric_option]>0].sort_values(metric_option,ascending=True).head(3)
    elif (metric_option in ('5 Year Average Dividend Yield %','Market Capitalization')):
        #print("based on "+metric_option+"\n")
        graph=yahoo_final.sort_values(metric_option,ascending=False).head(3)
    elif(metric_option=='Beta 5Y Monthly'):
        yahoo_final['mod']= abs(abs(yahoo_final[metric_option])-1)
        graph=yahoo_final[yahoo_final[metric_option]>0].sort_values('mod',ascending=True).head(3)
    else:
        graph=yahoo_final.sort_values(metric_option,ascending=False).head(3) 
    my_colors = ['g','b','r']
    fig, ax = plt.subplots()
    graph.plot(x='Company', y=metric_option,kind='bar',ax=ax,title='Top 3 stocks based on '+metric_option,xlabel='Company',ylabel=metric_option,color=my_colors,legend=False,rot=0)  
   
    table= graph[['Company','Symbol','Market Capitalization', '5 Year Average Dividend Yield %','PEG Ratio', 'PE Ratio', 'Beta 5Y Monthly','PBV Ratio']]
    table.drop(metric_option,axis=1,inplace=True)
    
    return table


  