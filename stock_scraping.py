from bs4 import BeautifulSoup
import pandas as pd
import datetime
import requests
import os

def get_content(content,class_path):
    get_content = content.find_all("tr",{'class':class_path})
    return get_content

def get_stock_price():
    r = requests.get("https://finance.yahoo.com/most-active/?count=100&offset=0")
    web_content = BeautifulSoup(r.text,'lxml')
    tr = get_content(web_content,'simpTblRow Bgc($hoverBgColor):h BdB Bdbc($seperatorColor) Bdbc($tableBorderBlue):h H(32px) Bgc($lv2BgColor)')
    tr2 = get_content(web_content,'simpTblRow Bgc($hoverBgColor):h BdB Bdbc($seperatorColor) Bdbc($tableBorderBlue):h H(32px) Bgc($lv1BgColor)')
    stock_lists =[]
    for i in range(0,13):
        td = tr[i].find_all('td')
        texts = [t.get_text() for t in td[1:5]]
        stock_lists.append(texts)
    for i in range(0,12):
        td = tr2[i].find_all('td')
        texts = [t.get_text() for t in td[1:5]]
        stock_lists.append(texts)
    df = pd.DataFrame(stock_lists,columns=['Name','Price','Change','%Change'])

    time_stamp = datetime.datetime.now()
    time_stamp = time_stamp.strftime('%Y-%m-%d')
    path = os.path.dirname(os.path.realpath(__file__))
    df.to_csv(os.path.join(path,"results/",str(time_stamp)+' stock data.csv'),mode='a',header=False)
    print(df)

if __name__ == "__main__":
    get_stock_price()