# Team Members:

# Kirtiman Rai |  kirtimar@andrew.cmu.edu

# Mihir Rao | msrao@andrew.cmu.edu

# Soumya Ruraraju | srudrara@andrew.cmu.edu

# Sudheeshna Sampath | sudheess@andrew.cmu.edu


#Description: This module is used to generate live web scraped data. It calls get_varables function under
#yahoo_web_scraping module to scrape the data and convert it into a beautifully formatted dataframe



#calling live web scrapped data module 
import yahoo_webscraping_module as ym

#get required info from web scrapped data
def get_live_webscraping(Company):
    
    stock_option=ym.getSymbolFromCompany(Company)
    bo=ym.get_variables(stock_option)

    bo.rename({'market_cap_in_trillions':'Market Capitalization','dividend_yield_in_perc':'5 Year Average Dividend Yield %',
           'PEG_ratio':'PEG Ratio','Trailing P/E':'PE Ratio','Beta':'Beta 5Y Monthly'},axis=1,inplace=True)
    
    bo=bo[['Company','Market Capitalization','5 Year Average Dividend Yield %','PEG Ratio','Beta 5Y Monthly','PE Ratio','price']]
    
    return bo

##Debugging code to check if the function is working properly
if __name__=='__main__':
    check_live=get_live_webscraping('LAM RESEARCH CORPORATION.')
    print(check_live)
