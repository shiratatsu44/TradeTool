from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

def fn_test(url):

      #変数設定
      a,b,c,d,e,f  = [],[],[],[],[],[] #リストを６つ用意
      df = pd.DataFrame() #取得結果格納用のデータフレーム

      #ページの閲覧
      html = urlopen(url)
      bsObj = BeautifulSoup(html, "html.parser")    
      tbl3 = bsObj.findAll("table")[3]
      trs = tbl3.findAll("tr")

      for tr in trs:
            lst=[]
            tds = tr.findAll('td') 
            for td in tds:
                  #各tdの値を各リストに各々格納
                  if td.get("class")[1] =="kjTime":a += [td.text ] #開示時刻
                  if td.get("class")[1] =="kjCode":b += [td.text ] #コード
                  if td.get("class")[1] =="kjName":c += [td.text ] #社名
                  if td.get("class")[1] =="kjTitle":d += [td.text ] #表題
                  if td.get("class")[1] =="kjTitle": #pdfのリンクURL
                      e += [td.a.get("href") ] if td.a is not None else [td.a ] 
                  if td.get("class")[1] =="kjXbrl" : #XBRLのDLリンク
                      f += [td.a.get("href") ] if td.a  is not None else [td.a ] 

      #取得結果格納リスト群からデータフレーム生成
      df = pd.DataFrame(
              data={'A': a, 'B': b, 'C': c, 'D': d, 'E': e, 'F': f},
              columns=['A', 'B', 'C', 'D', 'E', 'F'])        
      return df 

# 日付
date = '20190426' #900件超
#date = '20190502' #0件
#date = '20190506' #1件

# URL文字列の生成
url0 = 'https://www.release.tdnet.info/inbs/'
url1 = url0  +  'I_list_{}_{}.html'.format('001',date)

# 該当URLを閲覧
html = urlopen(url1)
bsObj = BeautifulSoup(html, "html.parser")
tbl1 = bsObj.findAll("table")[1]

dv1 = tbl1.findAll("div",{"class":"kaijiSum"})
dv2 = tbl1.findAll("div",{"class":"pager-O"})
dv3 = tbl1.findAll("div",{"class":"pager-M"})

if dv1 ==[]:
   print('開示0件')
else:
    print(str(dv1).split('全')[1].split('</')[0])
    lst =[ int(i.string) for i in dv3]
    if lst ==[]:
        df  = fn_test(url1)    
        print(df)
    else:
        # ページ数の取得
        mxpg= max(lst) 
        print( mxpg ) 

        # 再度URL文字列の生成
        for i in range(mxpg):
              s = str(i + 1)
              url1= url0  + 'I_list_{}_{}.html'.format(s.zfill(3) ,date)      
              print(s , url1)

              # ページを逐次閲覧して開示情報を取得
              df = fn_test(url1)
              print(df)
