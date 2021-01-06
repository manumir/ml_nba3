import pandas as pd

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


coef=0.1 #input('coef: ')
models=['','model_linear20.csv','model_linear60.csv','model_nn20.csv','nn60.csv']
mode=int(input('which model\n1:linear20   2:linear60   3:nn20   4:nn60\n'))

lin=pd.read_csv(models[mode])
print('using',models[mode])

count,beted=0,0
for x in range(len(lin)):
	date=lin.iloc[x]['date']
	home=lin.iloc[x]['home']
	away=lin.iloc[x]['away']
	lpred=lin.iloc[x]['pred']
	
	game=plac.loc[plac['date']==date]
	game=game.loc[game['home']==home]
	game=game.reset_index(drop=True)

	if date == 20210105:

		myodd=round(1/lpred,2)*float(coef) + round(1/lpred,2)
		if myodd < game['plac_A'].values[0]:
			print(date,home,away,'bet on away')

		myodd=round(1/(1-lpred),2)*float(coef) + round(1/(1-lpred),2)
		if myodd < game['plac_H'].values[0]:
			print(date,home,away,'bet on home')

	result=df.loc[df['date']==date]
	if len(result) > 0:
		result=result.loc[result['team']==home]['result'].values[0]	

		myodd=round(1/lpred,2)*float(coef) + round(1/lpred,2)
		if myodd < game['plac_A'].values[0]:
			if result == 1:
				count=count+float(game['plac_A'].values[0])
			beted=beted+1
			#print(game,'my odd:',1/lpred,1,'result:',result)

		myodd=round(1/(1-lpred),2)*float(coef) + round(1/(1-lpred),2)
		if myodd < game['plac_H'].values[0]:
			if result == 0:
				count=count+float(game['plac_H'].values[0])
			beted=beted+1
			#print(game,lpred,result)
		#print(game,lpred)
print('won:',count,'spent:',beted,'profit:',count-beted,(count-beted)/count * 100,'%')

