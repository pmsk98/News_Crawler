# -*- coding: utf-8 -*-
"""
Created on Mon Oct 11 17:17:35 2021

@author: user
"""




import pandas as pd
import glob
import os
import natsort


input_file = r'C:/Users/user/Desktop/졸업논문코드/삼성전자_뉴스/'# csv파일들이 있는 디렉토리 위치
output_file = r'C:/Users/user/Desktop/졸업논문코드/삼성전자_뉴스/samsung_news.csv'# 병합하고 저장하려는 파일명

allFile_list = glob.glob(os.path.join(input_file, 'page*')) # glob함수로 sales_로 시작하는 파일들을 모은다
print(allFile_list)
allFile_list =natsort.natsorted(allFile_list)

print(natsort.natsorted(allFile_list))
allData = [] # 읽어 들인 csv파일 내용을 저장할 빈 리스트를 하나 만든다
for file in allFile_list:
    df = pd.read_csv(file) # for구문으로 csv파일들을 읽어 들인다
    allData.append(df) # 빈 리스트에 읽어 들인 내용을 추가한다

dataCombine = pd.concat(allData, axis=0, ignore_index=True) # concat함수를 이용해서 리스트의 내용을 병합
# axis=0은 수직으로 병합함. axis=1은 수평. ignore_index=True는 인데스 값이 기존 순서를 무시하고 순서대로 정렬되도록 한다.
dataCombine.to_csv(output_file, index=False) # to_csv함수로 저장한다. 인데스를 빼려면 False로 설정



