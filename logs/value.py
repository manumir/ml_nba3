import sys
import pandas as pd
import matplotlib.pyplot as plt

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


models=['model_linear20.csv','model_linear60.csv','model_nn20.csv','nn60.csv']
mode=int(input('which model: | 0:linear20 | 1:linear60 | 2:nn20 | 3:nn60 |: '))

lin=pd.read_csv(models[mode])
print('--------- USING',models[mode],'---------------')

coef=0.2 #input('coef: ')
count,beted=0,0
dates,profits=[],[]
for x in range(len(lin)):
	date=lin.iloc[x]['date']
	home=lin.iloc[x]['home']
	away=lin.iloc[x]['away']
	lpred=lin.iloc[x]['pred']

	game=plac.loc[plac['date']==date]
	game=game.loc[game['home']==home]
	game=game.reset_index(drop=True)

	if len(sys.argv) == 2 and len(game)>0:
		if date == int(sys.argv[1]):

			myodd=round(1/lpred,2)
			myodd=myodd+myodd*coef
			if myodd < game['plac_A'].values[0]:
				print(date,home,away,'bet on',away)

			myodd=round(1/(1-lpred),2)
			myodd=myodd+myodd*coef
			if myodd < game['plac_H'].values[0]:
				print(date,home,away,'bet on',home)
	if len(game)==0:
		print("can't calculate/use the",home,'vs',away,'game')
		print("either a game's odds are missing or the command argument is missing")

	game_stats=df.loc[df['date']==date]
	if len(game_stats) > 0:
		try:
			result=game_stats.loc[game_stats['team']==home]['result'].values[0]	
		except:
			print(home)
		OVERTIME=game_stats.loc[game_stats['team']==home]['MP'].values[0]	

		myodd=round(1/lpred,2)
		myodd=myodd+myodd*coef

		if myodd < game['plac_A'].values[0]:
			if result == 1 and OVERTIME == '240':
				count=count+float(game['plac_A'].values[0])
			beted=beted+1
			#print(game,'my odd:',1/lpred,1,'result:',result)

		myodd=round(1/(1-lpred),2)
		myodd=myodd+myodd*coef
		if myodd < game['plac_H'].values[0]:
			if result == 0 and OVERTIME == '240':
				count=count+float(game['plac_H'].values[0])
			beted=beted+1
			#print(game,lpred,result)
		#print(game,lpred)
	#dates.append(date)
	try:
		profits.append(round((count-beted)/(count) *100,2))
	except:
		profits.append(round((count-beted)/(count+1) *100,2))
print('############## RESULTS ##########\nwon:',round(count,2),'| spent:',beted,'| profit:',round(count-beted,2),'|',round((count-beted)/count * 100,2),'%')

plt.xlabel('games')
plt.ylabel('return in percentage')
plt.plot(profits)
plt.savefig("mygraph.png")
print('saved graph to mygraph.png')
