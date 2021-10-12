#plot price trends in plotly based on company chosen in dropdown

###Team Members:
# 1)Kirtiman Rai |  kirtimar@andrew.cmu.edu

# 2)Mihir Rao | msrao@andrew.cmu.edu

# 3)Soumya Ruraraju | srudrara@andrew.cmu.edu

# 4)Sudheeshna Sampath | sudheess@andrew.cmu.edu
###

##This module plots the interactive stock chart showing stock prices trend and gives user the option to see the price trends for the previous one year, six months or one month ##


import pandas as pd
###Importing Plotly and all its dependencies for plotting the interactive stock price chart###
import plotly
import plotly.express as px
import plotly.io as pio
pio.renderers.default='svg'
from plotly.offline import download_plotlyjs, init_notebook_mode,  plot
import plotly.graph_objs  as po
from plotly.offline import plot

#a is company chosen
def PriceChart(a):
    path1="Market_Screener_FInal_File.csv"
    df1=pd.read_csv(path1)
    
    path2="google_finance_dataset.csv"
    df2=pd.read_csv(path2)
    
    df2=df2.merge(df1[['Symbol','Company']],how='left',left_on='STOCK',right_on='Symbol')
    
    ls=df2['Company'].unique()
    ls
    
    df2['DATE']=pd.to_datetime(df2['DATE'])
    
    df2['TIMESTAMP']=df2['DATE'].dt.date
    final_graph=pd.DataFrame(df2[df2['Company']==a])
    
    final_graph.drop(columns=['DATE','STOCK'],axis=1)
    
    #import plotly.express as px
    
    fig = po.Figure(px.line(final_graph, x='DATE', y='PRICE', title='Price Chart for '+a))

    fig.update_xaxes(
     rangeslider_visible=True,
     rangeselector=dict(
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")
        ])
        )
    )
    return fig
    
PriceChart('APPLE INC.')