import pandas as pd
import matplotlib.pyplot as plt

df=pd.read_csv('../data/season_start.csv')

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

plac=pd.read_csv('plac_log.csv')

new=[]
for date in plac['date']:
	month=date[:2]
	day=date[3:5]
	year=date[6:]
	new.append(int(year+month+day))
plac['date']=new	

new=[]
for x in range(len(plac)):
	if plac.at[x,'plac_H'] > plac.at[x,'plac_A']:
		new.append(1)
	else:
		new.append(0)
plac['pred']=new

count,total=0,0
profits=0
profits1=[]
for x in range(len(plac)):
	date=plac.iloc[x]['date']
	home=plac.iloc[x]['home']
	away=plac.iloc[x]['away']
	
	game=df.loc[df['date']==date]
	game=game.loc[game['team']==home]
	game=game.reset_index(drop=True)
	
	if len(game) > 0:
		result=game.iloc[0]['result']
		#print(date,home,away,plac.iloc[x]['pred'],'result',game.iloc[0]['result'])
		if plac.iloc[x]['pred']==result:
			count=count+1
		total=total+1
		if plac.iloc[x]['pred'] == 1:
			profits=profits-1
			if result == 0:
				profits=profits+plac.iloc[x]['plac_H']
		if plac.iloc[x]['pred'] == 0:
			profits=profits-1
			if result == 1:
				profits=profits+plac.iloc[x]['plac_A']

	profits1.append(profits)
print('betting only on underdogs gives:{} at {}% roi'.format(profits,round(profits/len(plac),3)))
plt.plot(profits1[::5])
#plt.show() # uncomment to show plot of underdogs
print('count:',count,'total:',total,'plac accuracy',count/total)

lin=pd.read_csv('model_linear20.csv')
count,total=0,0
for x in range(len(lin)):
	date=lin.iloc[x]['date']
	home=lin.iloc[x]['home']
	away=lin.iloc[x]['away']
	
	game=df.loc[df['date']==date]
	game=game.loc[game['team']==home]
	game=game.reset_index(drop=True)
	#print(date,home,away,game.iloc[0]['result'],round(lin.at[x,'pred']))

	if len(game) > 0:
		if game.iloc[0]['result']==round(lin.at[x,'pred']):
			count=count+1
		total=total+1
print('count:',count,'total:',total,'model_linear20 acc',count/total)

nn=pd.read_csv('model_nn20.csv')
count,total=0,0
for x in range(len(nn)):
	date=nn.iloc[x]['date']
	home=nn.iloc[x]['home']
	away=nn.iloc[x]['away']
	
	game=df.loc[df['date']==date]
	game=game.loc[game['team']==home]
	game=game.reset_index(drop=True)
	#print(home,away,game.iloc[0]['result'],round(nn.at[x,'pred']))

	if len(game) > 0:
		if game.iloc[0]['result']==round(nn.at[x,'pred']):
			count=count+1
		total=total+1
print('count:',count,'total:',total,'model_nn20 acc',count/total)

lin=pd.read_csv('model_linear60.csv')
count,total=0,0
for x in range(len(lin)):
	date=lin.iloc[x]['date']
	home=lin.iloc[x]['home']
	away=lin.iloc[x]['away']
	
	game=df.loc[df['date']==date]
	game=game.loc[game['team']==home]
	game=game.reset_index(drop=True)
	#print(home,away,game.iloc[0]['result'],round(lin.at[x,'pred']))

	if len(game) > 0:
		if game.iloc[0]['result']==round(lin.at[x,'pred']):
			count=count+1
		total=total+1

print('count:',count,'total:',total,'model_linear60 acc',count/total)

lin=pd.read_csv('nn60.csv')
count,total=0,0
for x in range(len(lin)):
	date=lin.iloc[x]['date']
	home=lin.iloc[x]['home']
	away=lin.iloc[x]['away']
	
	game=df.loc[df['date']==date]
	game=game.loc[game['team']==home]
	game=game.reset_index(drop=True)
	#print(home,away,game.iloc[0]['result'],round(lin.at[x,'pred']))

	if len(game) > 0:
		if game.iloc[0]['result']==round(lin.at[x,'pred']):
			count=count+1
		total=total+1

print('count:',count,'total:',total,'nn60 acc:',count/total)

lin=pd.read_csv('xgb20.csv')
count,total=0,0
for x in range(len(lin)):
	date=lin.iloc[x]['date']
	home=lin.iloc[x]['home']
	away=lin.iloc[x]['away']
	
	game=df.loc[df['date']==date]
	game=game.loc[game['team']==home]
	game=game.reset_index(drop=True)
	#print(home,away,game.iloc[0]['result'],round(lin.at[x,'pred']))

	if len(game) > 0:
		if game.iloc[0]['result']==round(lin.at[x,'pred']):
			count=count+1
		total=total+1

print('count:',count,'total:',total,'xgb20 acc:',count/total)


lin=pd.read_csv('nn40wr.csv')
count,total=0,0
for x in range(len(lin)):
	date=lin.iloc[x]['date']
	home=lin.iloc[x]['home']
	away=lin.iloc[x]['away']
	
	game=df.loc[df['date']==date]
	game=game.loc[game['team']==home]
	game=game.reset_index(drop=True)
	#print(home,away,game.iloc[0]['result'],round(lin.at[x,'pred']))

	if len(game) > 0:
		if game.iloc[0]['result']==round(lin.at[x,'pred']):
			count=count+1
		total=total+1

print('count:',count,'total:',total,'nn40wr acc:',count/total)


