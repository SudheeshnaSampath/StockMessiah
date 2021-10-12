"""
Stock Messiah (Group 12) Source Code

"""
#importing required packages
from tkinter import *
from tkinter import ttk

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm

import numpy as np
import pandas as pd

import plotly
import plotly.express as px
import plotly.io as pio
pio.renderers.default='svg'
from plotly.offline import download_plotlyjs, init_notebook_mode,  plot
import plotly.graph_objs  as po
from plotly.offline import plot

#importing required modules
import Recommendation as rcm
import getPriceChart as gpc
import StockScreener as ss
import live_web_scraping as lws

#calling tkinter window
mainw=Tk()

#Title
Label(mainw,text = "Welcome to Stock Messiah!",font=("Helvetica", 18)).grid(row=0,column=10,padx=40,pady =2)
#sub-title
Label(mainw,text = "Stock Messiah will aid your decision making based on your preferences!").grid(row=2,column=10)

#explanation text for view dropdown
Label(mainw,text = "Choose what you want to view: ").grid(row=6,column=8)


#read data from yahoo finance
marketscreener=pd.read_csv('Market_Screener_FInal_File.csv')
companies = marketscreener['Company'].unique()

#create frame for the visualizations
frame=Frame(mainw)
frame.grid(row=20,column=10)

#display recommendation if 'recommendation' dropdown is chosen
def displayRecco(str1):
    x=Label(frame,text = 'Based on your choice, Stock Messiah recommends investing in '+str1,font=("Helvetica", 12))
    x.config(width=100)
    x.grid(row=20,column=10)

#display stock details table if 'Stock Details (Live Web Scrapping)' dropdown is chosen    
def displayLiveChart(table1):
    tree = ttk.Treeview(frame,selectmode="extended",height=6)
    tree.grid(row=20,column=10)
    cols=list(table1.columns)
    tree["columns"] = cols
    
    tree.column("#0", width=0)
    #tree.column("Company",width=220)
    
    for i in cols:
        tree.column(i,  minwidth=0, width=120, stretch=NO)
        tree.column("Company",width=220)
        tree.heading(i, text=i, anchor='w')
    
    for index, row in table1.iterrows():
        tree.insert("",0,text=index,values=list(row))
    
#display stock chart(for top 3) and table if 'Stock Screener (Previously web scrapped)' is choosen    
def displayStockChart(fig1,table1):
    canvas = FigureCanvasTkAgg(fig1,frame)  
    canvas.get_tk_widget().grid(row=20,column=10)
    canvas.draw()

    tree = ttk.Treeview(frame,selectmode="extended",height=6)
    tree.grid(row=26,column=10)
    cols=list(table1.columns)
    tree["columns"] = cols
    
    tree.column("#0", width=0)
    
    for i in cols:
        tree.column(i,  minwidth=0, width=130, stretch=NO)
        tree.column("Company",width=220,stretch=YES)
        tree.heading(i, text=i, anchor='w')

    for index, row in table1.iterrows():
        tree.insert("",0,text=index,values=list(row))
  
#plot price trends on plotly if 'Price Trends' is choosen    
def displayPriceTrends(fig):
     plot(fig)


#show options and call functions based on view dropdown
def viewResponse(event):
    
    #clear frame each time button is pressed
    frame.but = Button(frame, text="clear before selecting New View", command=clearFrame)
    frame.but.grid(row=4, column=10, padx=10, pady=5) 
    
    if(n1.get()=='Recommendation'):
        x=Label(mainw,text = 'Pick a Stock Metric you want to filter recommendation by', width=50).grid(row=15,column=8)
        #metric dropdown   
        chosenMetricX = OptionMenu(mainw, n2, *metrics,command=lambda x: displayRecco(rcm.viewRecco(n2.get())))
        chosenMetricX.config(width=50)
        chosenMetricX.grid(row=15,column=10)

    elif(n1.get()=='Stock Details (Live Web Scrapping)'):
        Label(mainw,text = 'Choose a Company\ to view its Live Stock Information', width=50).grid(row=15,column=8,padx=50)
        #company dropdown
        chosenMetricLive = OptionMenu(mainw, n3, *companies,command=lambda x: displayLiveChart(lws.get_live_webscraping(n3.get())))
        chosenMetricLive.config(width=50)
        chosenMetricLive.grid(row=15,column=10)
        
    elif(n1.get()=='Stock Screener (Previously web scrapped)'):
        Label(mainw,text = 'Pick a Stock metric you want to screen top 3 stocks for', width=50).grid(row=15,column=8) 
        #metric dropdown
        chosenMetricY = OptionMenu(mainw, n2, *metrics,command=lambda x: displayStockChart(ss.get_graph(n2.get()),ss.get_table(n2.get())))  
        chosenMetricY.config(width=50)
        chosenMetricY.grid(row=15,column=10)
        
    else:
        Label(mainw,text = 'Choose a Company\'s Stock to view its Price Trends', width=50).grid(row=15,column=8,padx=50)
        #company dropdown
        chosenMetricZ = OptionMenu(mainw, n3, *companies,command=lambda x: displayPriceTrends(gpc.PriceChart(n3.get())))
        chosenMetricZ.config(width=50)
        chosenMetricZ.grid(row=15,column=10)
 
#function to clear widgets in frame
def clearFrame():
    for widget in frame.winfo_children():
       widget.destroy()
 
#metric dropdown
metrics = ['PE Ratio','PEG Ratio','Market Capitalization','PBV Ratio','Beta 5Y Monthly','5 Year Average Dividend Yield %']
n2 = StringVar(mainw) 
n2.set(metrics[0])

#company dropdown
n3 = StringVar(mainw) 
n3.set(companies[0])
  
#view dropdown
view = ['Recommendation','Stock Details (Live Web Scrapping)','Stock Screener (Previously web scrapped)','Price Trends']
n1 = StringVar(mainw) 
n1.set(view[0])
chosenTask = OptionMenu(mainw, n1, *view, command = viewResponse)
chosenTask.grid(row=6,column=10,padx=40,pady=30)

#set tkinter window details
mainw.title("STOCK MESSIAH")
mainw.geometry('2000x2000')
mainw.mainloop()