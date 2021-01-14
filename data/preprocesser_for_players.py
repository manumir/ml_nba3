import pandas as pd
import numpy as np
import functions as f
import time

start=time.time()
df=pd.read_csv('all_data.txt')
#df=pd.read_csv('data19-20.txt')

#df.pop('drop_this')

for x in range(len(df)):
	if df.at[x,'FG']==0 and df.at[x,'FGA']==0:
		df.at[x,'FG%']=0
	if df.at[x,'FT']==0 and df.at[x,'FTA']==0:
		df.at[x,'FT%']=0
	if df.at[x,'3P']==0 and df.at[x,'3PA']==0:
		df.at[x,'3P%']=0
	if pd.isnull(df.at[x,'+/-']):
		df.at[x,'+/-']=0

del2=[]
for x in range(len(df)):
	if df.at[x,'MP'] in ['Did Not Play','Did Not Dress','Not With Team','Player Suspended']:
		del2.append(x)
df=df.drop(del2)
df=df.reset_index(drop=True)

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

# make a game id column
x,i=0,0
ids=[]
count=0
while x < len(df):
	home=df.at[x,'team']    
	date=df.at[x,'date']

	df_2=df.loc[df['date'] == date]
	df_2=df_2.loc[df_2['team'] == home]

	x=df_2.tail(1).index[0]+1
	i=i+0.5
  
	count=count+len(df_2)
	if i % 1 == 0:
		for j in range(count):
			ids.append(int(i))
		count=0
df['gameid']=ids

### make a result column
x=0
new=[]
while x < len(df):
	date=df.at[x,'date']
	away=df.at[x,'team']

	df2=df.loc[df['date'] == date]

	df_away=df2.loc[df2['team'] == away]
	away_pts=df_away.tail(1)['PTS'].values[0]

	home_name=df.at[df_away.tail(1).index[0]+1,'team']
	df_home=df2.loc[df2['team']== home_name]
	home_pts=df_home.tail(1)['PTS'].values[0]

	if away_pts-home_pts > 0:
		for x in range(len(df_away)+len(df_home)):
			new.append(1)
	else:
		for x in range(len(df_away)+len(df_home)):
			new.append(0)

	x=df_home.tail(1).index[0]+1
df['Result']=new

# delete lines that have the totals of each team and players that DNP (did not play)
del2=[]
for x in range(len(df)):
	if df.at[x,'player'] == 'Team Totals':
		del2.append(x)
df=df.drop(del2)
df.reset_index(drop=True,inplace=True)

# change MIN column to int
new=[]
for x in range(len(df)):
	a=df.at[x,'MP']
	a=int(a[:a.find(':')])
	b=df.at[x,'MP']
	b=int(b[b.find(':')+1:])
	new.append(((a*60)+b)/60)
df['MP']=new

### change team names to acronimo
"""
new=[]
for team in df['team']:
	new.append(f.name2acro(team))
df['team']=new
"""

### check for nan rows
nan_rows = df[df.isnull().T.any().T]
print(nan_rows)

## sort by date and game id
df=df.sort_values(by=['date','gameid'])

## columns to average
cols=['MP','FG','FGA','FG%','3P','3PA','3P%','FT','FTA','FT%','ORB','DRB','TRB','AST','TOV','STL','BLK','PF','PTS','+/-']

og=df.copy()
for x in range(len(df)):
	team=df.at[x,'team']
	player=df.at[x,'player']
	date=df.at[x,'date']

	df_2=og.loc[og['player'] == player]
	df_2.reset_index(drop=True,inplace=True)

	df_2=df_2.loc[df_2['date'] < date]
	df_2.reset_index(drop=True,inplace=True)

	df_2=df_2.loc[df_2['team'] == team]
	df_2.reset_index(drop=True,inplace=True)

	df_2=df_2.tail(15)

	if len(df_2) > 0:
		for col in cols:
			y=0
			for value in df_2[col]:
				#if value == '-': # doesn't work
				#	value = 0 # idk why
				y=y+float(value)

			avg=y/len(df_2)
			df.at[x,col]=avg
	if x % 1024 == 0:
		print(x)

print(df)

df.to_csv(input('name of file to output: '),index=False)

print(time.time()-start)


