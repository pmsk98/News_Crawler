
from bs4 import BeautifulSoup
from datetime import datetime
import requests
import pandas as pd
import re
import time
#날짜 정제화 함수
def date_cleansing(test):
    try:
        #지난 뉴스
        #머니투데이  10면1단  2018.11.05.  네이버뉴스   보내기  
        pattern = '\d+.(\d+).(\d+).'  #정규표현식 
    
        r = re.compile(pattern)
        match = r.search(test).group(0)  # 2018.11.05.
        date_text.append(match)
        
    except AttributeError:
        #최근 뉴스
        #이데일리  1시간 전  네이버뉴스   보내기  
        pattern = '\w* (\d\w*)'     #정규표현식 
        
        r = re.compile(pattern)
        match = r.search(test).group(1)
        #print(match)
        date_text.append(match)


#내용 정제화 함수 
def contents_cleansing(contents):
    first_cleansing_contents = re.sub('<dl>.*?</a> </div> </dd> <dd>', '', 
                                      str(contents)).strip()  #앞에 필요없는 부분 제거
    second_cleansing_contents = re.sub('<ul class="relation_lst">.*?</dd>', '', 
                                       first_cleansing_contents).strip()#뒤에 필요없는 부분 제거 (새끼 기사)
    third_cleansing_contents = re.sub('<.+?>', '', second_cleansing_contents).strip()
    contents_text.append(third_cleansing_contents)
    #print(contents_text)
    

start=1
title_text=[]
link_text=[]
source_text=[]
date_text=[]
contents_text=[]
result={}

while True:
    try:
        url = 'https://search.naver.com/search.naver?where=news&sm=tab_pge&query=%EC%82%BC%EC%84%B1%EC%A0%84%EC%9E%90&sort=2&photo=0&field=0&pd=3&ds=2016.01.01&de=2020.12.31&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:from20160101to20201231,a:all&start={}'.format(start)
        headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
          'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}
        response = requests.get(url, headers=headers)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        #<a>태그에서 제목과 링크주소 (a 태그 중 class 명이 news_tit인 것)
       #<a>태그에서 제목과 링크주소 추출
        atags = soup.select('.news_tit')
        for atag in atags:
            title_text.append(atag.text)     #제목
            link_text.append(atag['href'])   #링크주소
        
        #신문사 추출
        source_lists = soup.select('.info_group > .press')
        for source_list in source_lists:
            source_text.append(source_list.text)    #신문사
        
        #날짜 추출 
        date_lists = soup.select('.info_group > span.info')
        for date_list in date_lists:
            # 1면 3단 같은 위치 제거
            if date_list.text.find("면") == -1:
                date_text.append(date_list.text)
        
        #본문요약본
        contents_lists = soup.select('.news_dsc')
        for contents_list in contents_lists:
            contents_cleansing(contents_list) #본문요약 정제화
        
        
        #모든 리스트 딕셔너리형태로 저장
        result= {"date" : date_text , "title":title_text ,  "source" : source_text ,"contents": contents_text ,"link":link_text }  
        
        df = pd.DataFrame(result)  #df로 변환
        
        
        start += 10
        time.sleep(0.5)
        print(start)
    
    except: # 오류발생시 몇 페이지까지 크롤링했는지 page를 확인하기 
        print(start)
        break

