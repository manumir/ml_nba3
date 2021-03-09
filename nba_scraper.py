#! /usr/bin/python3

# usage:

# scrape nba season 2008-2009:
# nba scraper.py 2008

# scrape nba playoffs 2008-2009:
# nba scraper.py 2008 'anything here'

import time
start_time = time.time()
import os
import sys

from selenium import webdriver
from bs4 import BeautifulSoup as bs4
import re 
import functions as f

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

year=str(sys.argv[1])

driver = webdriver.Chrome(executable_path='../chromedriver')
if len(sys.argv)<3:
	driver.get('https://stats.nba.com/teams/boxscores-traditional/?Season='+sys.argv[1]+'&SeasonType=Regular%20Season')
else:
	driver.get('https://stats.nba.com/teams/boxscores-traditional/?Season='+sys.argv[1]+'&SeasonType=Playoffs')

WebDriverWait(driver,25).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.banner-actions-container")))

path=driver.find_element_by_id("onetrust-accept-btn-handler")
path.click()

if len(sys.argv)<3:
	driver.get('https://stats.nba.com/teams/boxscores-traditional/?Season='+sys.argv[1]+'&SeasonType=Regular%20Season')
else:
	driver.get('https://stats.nba.com/teams/boxscores-traditional/?Season='+sys.argv[1]+'&SeasonType=Playoffs')

WebDriverWait(driver,15).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.nba-stat-table__overflow")))

file_name='nba_scraper_test.csv'
file=open(file_name,'w')
file.write('team,Match Up,date,W/L,MP,PTS,FG,FGA,FG%,3P,3PA,3P%,FT,FTA,FT%,ORB,DRB,TRB,AST,TOV,STL,BLK,PF,+/-,\n')

#print(NUMBER_OF_PAGES)
#for i in range(NUMBER_OF_PAGES):
html=bs4(driver.page_source,'html.parser')
#features = html.table.thead.tr.text #don't need to scrape this multiple times
stats=html.table.tbody
games=stats.find_all("tr")
for game in games:
	game_stats=game.find_all("td")
	for stat in game_stats:
		stat=stat.text
		stat=re.findall(r'\d+|\w+|@|/',stat)
		if len(stat)==3:
			stat=''.join(stat)
			stat=stat+','
		if len(stat)==5:
			stat=''.join(stat)
			stat=stat+','
		if len(stat)==2:
			stat=stat[0]+'.'+stat[1]+','
		if len(stat)==1:
			stat=''.join(stat)
			stat=stat+','
		if len(stat)!=0:
			file.write(stat)
	file.write('\n')

file.close()
driver.quit()
print("scraped in %s seconds" % (time.time() - start_time))

import pandas as pd

df=pd.read_csv(file_name)
df.pop('Unnamed: 24')

new=[]
for date in df['date']:
	year=date[-4:]
	day=date[3:5]
	month=date[:2]
	date=year+month+day
	new.append(date)
df['date']=new

df=df.loc[df['date']==sys.argv[2]]

### turn date column to int for compairson
new=[]
months=['January','February','March','April','May','June','July','August','September','October','November','December']
months_1=['01','02','03','04','05','06','07','08','09','10','11','12']
for date in df['date']:
	date=str(date)
	year=date[:4]
	day=date[-2:]
	month=date[4:6]
	for name in months_1:
		if month == name:
			ix=months_1.index(name)
			new.append(months[ix]+' '+day+' '+year)
df['date']=new

new=[]
for x in df['MP']:
	if x == 48:
		x=240
	else:
		x=290
	new.append(x)
df['MP']=new

df=df.reset_index(drop=True)
home,away=[],[]
for x in range(len(df)):
	if df.at[x,'W/L'] == 'L':
		df.at[x,'+/-'] = str(-int(df.at[x,'+/-']))
	if '@' in df.at[x,'Match Up']:
		away.append(x)
	else:
		home.append(x)

home=df.loc[home]
away=df.loc[away]

new=[]
for x in home['Match Up']:
	x=x[-3:]
	new.append(x)
home['Match Up']=new

new=[]
for x in away['Match Up']:
	x=x[-3:]
	new.append(x)
away['Match Up']=new

df=pd.DataFrame(columns=['team','Match Up','date','W/L','MP','PTS','FG','FGA','FG%','3P','3PA','3P%','FT','FTA','FT%','ORB','DRB','TRB','AST','TOV','STL','BLK','PF','+/-'])

# get away and home from the same game together, next to one another
home=home.reset_index(drop=True)
away=away.reset_index(drop=True)
for x in range(len(home)):
	home_team=home.at[x,'team']
	away_team=away.loc[away['Match Up']==home_team]
	index=int(away_team.index[0])
	df=df.append(pd.Series(away.iloc[index]),ignore_index=True)
	df=df.append(pd.Series(home.iloc[x]),ignore_index=True)

new=[]
for x in df['FT%']:
	x=round(x/100,3)
	new.append(x)
df['FT%']=new

new=[]
for x in df['FG%']:
	x=round(x/100,3)
	new.append(x)
df['FG%']=new

new=[]
for x in df['3P%']:
	x=round(x/100,3)
	new.append(x)
df['3P%']=new

new=[]
for x in range(len(df)):
	new.append('Team Totals')
df['player']=new

new=[]
for x in df['team']:
	new.append(f.name2acro(x))
df['team']=new

df=df[['date','team','player','MP','FG','FGA','FG%','3P','3PA','3P%','FT','FTA','FT%','ORB','DRB','TRB','AST','STL','BLK','TOV','PF','PTS','+/-']]

print(df)
df.to_csv(file_name,index=False)




