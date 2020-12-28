#!/usr/bin/env python3

import time
import datetime
start_time = time.time()

from selenium import webdriver
from bs4 import BeautifulSoup as bs4
import re
import pandas as pd
import functions as f
import os
import platform

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

os_name=platform.system()

if os_name=='Linux':
	driver = webdriver.Chrome(executable_path='../chromedriver')
else:
	driver = webdriver.Chrome(executable_path='C:/Users/dude/Desktop/chromedriver.exe')
driver.get('https://placard.jogossantacasa.pt/PlacardWeb/Events?CompetionName=&RegionName=&SelectedCompetitionId=&SelectedDate='+input('year-month-day(2020-08-04): ')+'&SelectedModalityId=basketball')

WebDriverWait(driver,15).until(EC.presence_of_element_located((By.ID, "b5-l4-0-b9-l1-0-b3-b10-$b2")))

html=bs4(driver.page_source,'html.parser')

nba_table=html.find_all("div",id='b5-l4-0-b8-SectionItem')

# teams field
teams=nba_table[0].find_all("span", class_="font-size20")

# odds field
odds=nba_table[0].find_all("span", class_="odd ThemeGrid_MarginGutter")

driver.quit()

### start preprocessing
home , away = [],[]
i=0
while i < len(teams):
	if i % 2 == 0:
		home.append(str(teams[i].text))
	else:
		away.append(str(teams[i].text))
	i=i+1

# get home and away odds
home_odds , away_odds=[],[]
i=0
while i < len(odds):
	odd=str(odds[i].text).replace(',','.')
	home_odds.append(float(odd))
	i=i+3
i=2
while i < len(odds):
	odd=str(odds[i].text).replace(',','.')
	away_odds.append(float(odd))
	i=i+3

# create date
today=datetime.date.today()
today=today.strftime("%m/%d/%Y")
date=[]
for x in range(len(home)):
    date.append(today)

df=pd.DataFrame()

new=[]
for name in home:
	new.append(f.name2acro(name))
df['home']=new

new=[]
for name in away:
	new.append(f.name2acro(name))
df['away']=new

df['date']=today
df['plac_H']=home_odds
df['plac_A']=away_odds

print(df)

curr_path=os.getcwd()
if os_name=='Linux':
	path2logs=curr_path+'/logs/'
else:
	path2logs=curr_path+'\\logs\\'

log=pd.read_csv(path2logs+'plac_log.txt')
log=log.append(df,sort=False)
log.to_csv(path2logs+'plac_log.txt',index=False)

