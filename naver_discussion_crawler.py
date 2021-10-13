# -*- coding: utf-8 -*-
"""
Created on Wed Oct 13 22:15:03 2021

@author: student
"""


# -*- coding: utf-8 -*-
"""
Created on Wed Oct 13 21:55:11 2021

@author: student
"""

import pandas as pd
from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import os 
from urllib.request import urlopen
import time


def naver_crawler(acode, page):
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'}
    total_dt = pd.DataFrame([])
    
    n_ = 0
    for page in range(1, page):
        
        n_ += 1
        if (n_ % 10 == 0):
            print('================== Page ' + str(page) + ' is done ==================')

        # url = "https://finance.naver.com/item/board.nhn?code=%s&page=%s" % (acode, page)
        url = "https://finance.naver.com/item/board.nhn?code=%s&page=%s" % (str(acode), str(page))

        result = requests.get(url, headers = headers)
        bs_obj = BeautifulSoup(result.content, "html.parser")
        table = bs_obj.find('table', {'class' : 'type2'})
        tt = table.select('tbody > tr')

        for i in range(2, len(tt)):
            if len(tt[i].select('td > span')) > 0:
              # print(i)
              date = tt[i].select('td > span')[0].text
              title = tt[i].select('td.title > a')[0]['title']
              writer = tt[i].select('td.p11')[0].text.replace('\t', '').replace('\n', '')
              views = tt[i].select('td > span')[1].text
              pos = tt[i].select('td > strong')[0].text
              neg = tt[i].select('td > strong')[1].text
              # print(date, title, writer, views, pos, neg)
              
              table = pd.DataFrame({'날짜' : [date], 
                                    '제목' : [title],
                                    '글쓴이' : [writer],
                                    '조회' : [views],
                                    '공감' : [pos],
                                    '비공감' : [neg]
                                    })
              total_dt = total_dt.append(table)
              time.sleep(0.005)
              print('{}페이지 완료'.format(n_))
    
    return total_dt


data= naver_crawler('000660',14751)


