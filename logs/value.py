import argparse
import sys
import pandas as pd
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument("-p","--plot", help="plot graph about returns")
parser.add_argument("-d","--day", help="date to see bets")
#parser.add_argument("-b","--both", help="prints stats about betting on homes and aways")
parser.add_argument("--home", help="prints stats about betting on homes only")
parser.add_argument("--away", help="prints stats about betting on aways only")
args = parser.parse_args()

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


models=['model_linear20.csv','model_linear60.csv','model_nn20.csv','nn60.csv','xgb20.csv','nn40wr.csv']
for model in models:
	lin=pd.read_csv(model)

	#coefs=[0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5] #input('coef: ')
	coefs=[0.1,0.2]
	for coef in coefs:
		count,beted=0,0
		right=0
		dates,profits=[0],[0]
		for date in sorted(list(set(lin['date']))):
			dategames=lin.loc[lin['date']==date]
			for x in range(len(dategames)):
				home=dategames.iloc[x]['home']
				away=dategames.iloc[x]['away']
				lpred=dategames.iloc[x]['pred']
				if lpred < 0:
					lpred=0.01

				game=plac.loc[plac['date']==date]
				game=game.loc[game['home']==home]
				try:
					A_odd=game['plac_A'].values[0]
					H_odd=game['plac_H'].values[0]

					A_myodd=round(1/lpred,2)*(coef+1)
					H_myodd=round(1/(1-lpred),2)*(coef+1)

					game_stats=df.loc[df['date']==date]
					if len(game_stats) > 0:
						result=game_stats.loc[game_stats['team']==home]['result'].values[0]	
						OVERTIME=game_stats.loc[game_stats['team']==home]['MP'].values[0]	

						if args.away or not args.home:
							if A_myodd < A_odd and A_odd > 2: # higher return on investement in percentage if i take odds > 2
								if result == 1 and OVERTIME == '240':
									count=count+A_odd
									right=right+1
								beted=beted+1
						# home
						if args.home or not args.away:
							if H_myodd < H_odd and H_odd > 2: # higher return on investement in percentage if i take odds > 2
								if result == 0 and OVERTIME == '240':
									count=count+H_odd
									right=right+1
								beted=beted+1

					if args.day and date == int(args.day):
						if args.away or not args.home:
							if A_myodd < A_odd and A_odd > 2:
								print(date,home,away,'bet on',away,A_myodd)
						if args.home or not args.away:
							if H_myodd < H_odd and H_odd > 2:
								print(date,home,away,'bet on',home,H_myodd)

				except Exception as e:
					print(e)
					print("can't calculate the",home,'vs',away,'on',date,'game check if we have the odds')
			
			#profits.append((count-beted)/beted) # to see if return has stabilized
			profits.append(round(count-beted,2)) # to see profit over time

		print(''+model,'|coef',coef,'|spent:',beted,'|profit:',round(count-beted,2),'|','\033[91m'+str(round((count-beted)/beted* 100,2))+'%\033[0m |',str(round(right/beted,2))+' got right')
		lastday=round(profits[len(profits)-2]-profits[-3],2)
		last7days=round(profits[len(profits)-2]-profits[-9],2)
		print('last 7 days',last7days,'| lastday (yesterday)',lastday,'\n')

		if args.plot:
			figure, axis = plt.subplots(1, 2) 
			axis[0].set_xlabel('day')
			axis[0].set_ylabel('profit €')
			axis[1].set_title('all time')
			axis[0].plot(profits)

			axis[1].set_xlabel('day')
			axis[1].set_ylabel('profit €')
			axis[1].set_title('last 7 days')
			axis[1].plot(profits[-9:])
			plt.show()
			#plt.savefig("mygraph.png")
			#print('saved graph to mygraph.png')

