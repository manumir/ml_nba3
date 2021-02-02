import sys
import pandas as pd
import numpy as np
import functions as f 
import joblib
import torch

df=pd.read_csv('../data/season_start.txt')

df=df.loc[df['player']=='Team Totals']
df.pop('player')
df=df.reset_index(drop=True)

#### process data
# fix +/- column
x=0
new=[]
while x < len(df):
	ptsA=df.at[x,'PTS']
	ptsH=df.at[x+1,'PTS']
	new.append(ptsH-ptsA)
	new.append(ptsA-ptsH)
	x=x+2
df['+/-']=new

location=[]
for x in range(len(df)):
	if x % 2 == 1:
		location.append(0)
	else:
		location.append(1)
df['location']=location

### make a result column
x,new=0,[]
while x < len(df):
	if float(df.at[x,'+/-']) < 0:
		new.append(1)
		new.append(1)
	else:
		new.append(0)
		new.append(0)
	x=x+2
df['result']=new

### turn date column to int for compairson
months=['January','February','March','April','May','June','July','August','September','October','November','December']
months_1=['01','02','03','04','05','06','07','08','09','10','11','12']
dates=list(df['date'].values)
new=[]
for x in range(len(df)):
	date=str(dates[x])
	date=date.split(' ')
	if len(date[1])==1:
		date[1]='0'+date[1]
	for name in months:
		if date[0] == name:
			ix=months.index(name)
			new.append(int(date[2]+months_1[ix]+date[1]))
df['date']=new

# change MIN column to int
new=[]
for x in range(len(df)):
	mp=df.at[x,'MP']
	min=int(mp[:mp.find(':')])
	sec=int(mp[mp.find(':')+1:])
	new.append(((min*60)+sec)/60)
df['MP']=new

### check for nan rows
#nan_rows = df[df.isnull().T.any().T]
#print(nan_rows)

## sort by date and game id
df=df.sort_values(by=['date'])

##### open games to predict
games=pd.read_csv('../schedule.csv')

### turn date column to int for compairson
months=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
months_1=['01','02','03','04','05','06','07','08','09','10','11','12']
dates=list(games['date'].values)
new=[]
for x in range(len(games)):
  date=str(dates[x])
  date=date.split(' ')[1:]
  if len(date[1])==1:
    date[1]='0'+date[1]
  for name in months:
    if date[0] == name:
      ix=months.index(name)
      new.append(int(date[2]+months_1[ix]+date[1]))
games['date']=new
#games_date=input('insert %year%month%day (e.g. 20200105): ')
games_date=sys.argv[1]
games=games.loc[games['date']==int(games_date)]

new=[]
for team in games['home']:
	new.append(f.name2acro(team))
games['home']=new

new=[]
for team in games['away']:
	new.append(f.name2acro(team))
games['away']=new

games=games.reset_index(drop=True)

########## open logs
## columns to average
cols=['MP','FG','FGA','FG%','3P','3PA','3P%','FT','FTA','FT%','ORB','DRB','TRB','AST','TOV','STL','BLK','PF','PTS','+/-']

MODEL='nn40wr'

WRITE=input('write to logs? y or n: ') 

if WRITE=='y':
	logs=open('../logs/'+MODEL+'.csv','a')

og=df.copy()
for x in range(len(games)):
	home=games.at[x,'home']

	df_2=og.loc[og['team'] == home]
	df_2=df_2.reset_index(drop=True)
	df_2=df_2.loc[df_2['date'] < int(games_date)]
	df_2.reset_index(drop=True,inplace=True)
	df_2=df_2.tail(40)

	rowH=[]
	if len(df_2) > 0:
		for col in cols:
			y=0
			for value in df_2[col]:
				y=y+float(value)
			avg=y/len(df_2)
			rowH.append(avg)

	# winrate here
	count=0
	for j in range(len(df_2)):
		if df_2.iloc[j]['result'] == 1 and df_2.iloc[j]['location'] == 1:
			count=count+1
		elif df.iloc[j]['result'] == 0 and df_2.iloc[j]['location'] == 0:
			count=count+1
	rowH.append(count/5)
	
	count=0
	df_2=df_2.tail(20)
	for j in range(len(df_2)):
		if df_2.iloc[j]['result'] == 1 and df_2.iloc[j]['location'] == 1:
			count=count+1
		elif df.iloc[j]['result'] == 0 and df_2.iloc[j]['location'] == 0:
			count=count+1
	rowH.append(count/5)
	
	count=0
	df_2=df_2.tail(10)
	for j in range(len(df_2)):
		if df_2.iloc[j]['result'] == 1 and df_2.iloc[j]['location'] == 1:
			count=count+1
		elif df.iloc[j]['result'] == 0 and df_2.iloc[j]['location'] == 0:
			count=count+1
	rowH.append(count/5)
	
	away=games.at[x,'away']
	
	df_2=og.loc[og['team'] == away]
	df_2=df_2.reset_index(drop=True)
	df_2=df_2.loc[df_2['date'] < int(games_date)]
	df_2.reset_index(drop=True,inplace=True)
	df_2=df_2.tail(40)

	rowA=[]
	if len(df_2) > 0:
		for col in cols:
			y=0
			for value in df_2[col]:
				y=y+float(value)
			avg=y/len(df_2)
			rowA.append(avg)
	
	count=0
	for j in range(len(df_2)):
		if df_2.iloc[j]['result'] == 1 and df_2.iloc[j]['location'] == 1:
			count=count+1
		elif df.iloc[j]['result'] == 0 and df_2.iloc[j]['location'] == 0:
			count=count+1
	rowA.append(count/5)
	# winrate here
	count=0
	df_2=df_2.tail(20)
	for j in range(len(df_2)):
		if df_2.iloc[j]['result'] == 1 and df_2.iloc[j]['location'] == 1:
			count=count+1
		elif df.iloc[j]['result'] == 0 and df_2.iloc[j]['location'] == 0:
			count=count+1
	rowA.append(count/5)
	
	count=0
	df_2=df_2.tail(10)
	for j in range(len(df_2)):
		if df_2.iloc[j]['result'] == 1 and df_2.iloc[j]['location'] == 1:
			count=count+1
		elif df.iloc[j]['result'] == 0 and df_2.iloc[j]['location'] == 0:
			count=count+1
	rowA.append(count/5)

	x=np.array(rowH)-np.array(rowA)
	x=x.reshape(1,-1)

	model=torch.load('./models/'+MODEL)
	x=torch.Tensor(x)
	print(games_date,home,away,float(model(x)))
	if WRITE == 'y':
		logs.write(str(games_date+','+home+','+away+','+str(float(model(x)))+'\n'))

logs.close()

