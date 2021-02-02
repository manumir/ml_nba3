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


models=['model_linear20.csv','model_linear60.csv','model_nn20.csv','nn60.csv','xgb20.csv','nn40wr.csv']
mode=int(input('which model: | 0:linear20 | 1:linear60 | 2:nn20 | 3:nn60 | 4: xgb20 |: '))

lin=pd.read_csv(models[mode])

#coefs=[0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5] #input('coef: ')
coefs=[0.25]
for coef in coefs:
	count,beted=0,0
	dates,profits=[0],[0]
	dates=sorted(list(set(lin['date'])))
	for date in dates:
		dategames=lin.loc[lin['date']==date]
		for x in range(len(dategames)):
			home=dategames.iloc[x]['home']
			away=dategames.iloc[x]['away']
			lpred=dategames.iloc[x]['pred']

			game=plac.loc[plac['date']==date]
			game=game.loc[game['home']==home]
			try:
				A_odd=game['plac_A'].values[0]
				H_odd=game['plac_H'].values[0]

				A_myodd=round(1/lpred,2)*(coef+1)
				H_myodd=round(1/(1-lpred),2)*(coef+1)

				if len(sys.argv) == 2 and date == int(sys.argv[1]):
					if A_myodd < A_odd:
						print(date,home,away,'bet on',away)
					if H_myodd < H_odd:
						print(date,home,away,'bet on',home)

				game_stats=df.loc[df['date']==date]
				if len(game_stats) > 0:
					result=game_stats.loc[game_stats['team']==home]['result'].values[0]	
					OVERTIME=game_stats.loc[game_stats['team']==home]['MP'].values[0]	

					if A_myodd < A_odd:
						if result == 1 and OVERTIME == '240':
							count=count+A_odd
						beted=beted+1
					if H_myodd < H_odd:
						if result == 0 and OVERTIME == '240':
							count=count+H_odd
						beted=beted+1
			except:
				print("can't calculate the",home,'vs',away,'on',date,'game')
				print('check if theres the game odds')
		
		profits.append(count-beted)


	print(coef,'won:',round(count,2),'| spent:',beted,'| profit:',round(count-beted,2),'|',round((count-beted)/beted* 100,2),'%')

plt.xlabel('day')
plt.ylabel('profit €')
plt.plot(profits)
#plt.show()
#plt.savefig("mygraph.png")
#print('saved graph to mygraph.png')
