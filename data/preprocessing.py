import pandas as pd
import numpy as np
import functions as f
import time
start=time.time()

df=pd.read_csv('all_data.txt')

df=df.loc[df['player']=='Team Totals']
df.pop('player')
df=df.reset_index(drop=True)

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
nan_rows = df[df.isnull().T.any().T]
print(nan_rows)

## sort by date and game id
df=df.sort_values(by=['date'])

## columns to average
cols=['MP','FG','FGA','FG%','3P','3PA','3P%','FT','FTA','FT%','ORB','DRB','TRB','AST','TOV','STL','BLK','PF','PTS','+/-']

og=df.copy()
for x in range(len(df)):
	team=df.at[x,'team']
	date=df.at[x,'date']

	df_2=og.loc[og['team'] == team]
	df_2=df_2.reset_index(drop=True)
	df_2=df_2.loc[df_2['date'] < date]
	df_2.reset_index(drop=True,inplace=True)
	df_2=df_2.tail(60)

	if len(df_2) > 0:
		for col in cols:
			y=0
			for value in df_2[col]:
				y=y+float(value)
			avg=y/len(df_2)
			df.at[x,col]=avg

		"""
		# winrate here
		count=0
		df_2=df_2.tail(5)
		for j in range(len(df_2)):
			if int(df.iloc[[j]].index[0]) % 2==0 and df.iloc[j]['result'] == 1:
				count=count+1
			elif int(df.iloc[[j]].index[0]) % 2==1 and df.iloc[j]['result'] == 0:
				count=count+1
		df.at[x,'wr5']=count/5
		"""
	if x % 1024 == 0:
		print(x)

# join rows
home,away=[],[]
for x in range(len(df)):
	if x % 2 == 1:
		home.append(x)
	else:
		away.append(x)

home=df.loc[home]
home=home.reset_index(drop=True)
away=df.loc[away]
away=away.reset_index(drop=True)

dates=home['date']
homes=home['team']
aways=away['team']
home=home.drop(['date','team'],1)
away=away.drop(['date','team'],1)
res=home['result']
df=home.subtract(away)
df['result']=res
df['home']=homes
df['away']=aways
df['date']=dates

#print(df.corr()['result'])

df.to_csv('train_test.csv',index=False)

print(time.time()-start)

