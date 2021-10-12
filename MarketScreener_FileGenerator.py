import pandas as pd

#reading the two input sheets
Main_Data = pd.read_excel (r'Market_Cat_rawfile.xlsx', sheet_name='main')
Mega_F = pd.read_excel (r'Market_Cat_rawfile.xlsx', sheet_name='megaF')

#removing extra spaces
Main_Data['Company']=Main_Data['Company'].apply(lambda x: x.strip())
Mega_F['Company']=Mega_F['Company'].apply(lambda x: x.strip())

#keeping only necessary column
Main_Data = Main_Data[['Company','Price']]
Mega_F = Mega_F[['Company', 'Symbol', 'Price (Intraday)', 'Flag']]

#removing punctuations to streamline merging
Main_Data['Company_new']= Main_Data['Company'].replace(r'[\,\.\;]','',regex=True)
Mega_F['Company_new']= Mega_F['Company'].replace(r'[\,\.\;]','',regex=True)

#Company words that can be in different for same company
problem_words = ['INC','CORPORATION','SO','INCORPORATED','LTD','IN','LIMITED','S','SOLUTIONS','INCORP','I','CORPOR','HOLD','HOLDI','HOLDINGS','CORPORA','CORPO','INTERNATIONAL','PLC', 'MACHINES']

#remove problem words
def check_pw(rows):
    if(rows['Company_new'].rsplit(" ",1)[-1] in problem_words):
        return rows['Company_new'].rsplit(" ",1)[0]
    else:
        return rows['Company_new']

#checking and removing
Main_Data['Company_new'] = Main_Data.apply(check_pw,axis=1)
Mega_F['Company_new'] = Mega_F.apply(check_pw,axis=1)
#rechecking
Main_Data['Company_new'] = Main_Data.apply(check_pw,axis=1)
Mega_F['Company_new'] = Mega_F.apply(check_pw,axis=1)

#removing extra spaces
Main_Data['Company_new']=Main_Data['Company_new'].apply(lambda x: x.strip())
Mega_F['Company_new']=Mega_F['Company_new'].apply(lambda x: x.strip())

#merge the two files to get required symbol and flag
MarketCap = Main_Data.merge(Mega_F,how='left',on='Company_new')

#remove unnecessary columns and rename as required
MarketCap = MarketCap.drop(['Company_y','Company_new'],axis=1)
MarketCap = MarketCap.rename(columns={'Company_x':'Company'})


MarketCap.to_csv('Market_Screener_FInal_File.csv')

