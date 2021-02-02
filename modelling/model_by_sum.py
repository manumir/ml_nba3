import pandas as pd
import functions as f 
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import joblib
import torch

"""
df=pd.read_csv('../data/train_players.csv')

columns2avg=['MP','FG','FGA','FG%','3P','3PA','3P%','FT','FTA','FT%','ORB','DRB','TRB','AST','STL','BLK','TOV','PF','PTS','+/-']

for x in range(len(df)):
	for column in columns2avg[1:]:
		df.at[x,column]=df.at[x,'MP']*df.at[x,column]
	if x % 50000 == 0:
		print(x)

train=pd.DataFrame(columns=df.columns)
j=0
for i in set(df['gameid']):
	df1=df.loc[df['gameid']==i]
	teams = df1['team'].unique()
	for team in teams:
		df2=df1.loc[df1['team']==team]
		df2=df2.reset_index(drop=True)
		df2=df2.sort_values(by=['MP'],ascending=False)
		df2=df2.head(8)

		for column in list(columns2avg):
			train.at[j,column]=sum(df2[column])
		train.at[j,'Result']=df2.head(1)['Result'].values[0]
		
		j=j+1
	if i % 1000 == 0:
		print(i)

train.to_csv('train_players8.csv',index=False)
"""

train=pd.read_csv('train_players8.csv')

train=train.drop(['gameid','date','team','player'],1)
train=train.reset_index(drop=True)

#train.pop('MP') # when scaled this is needed

home1,away1=[],[]
for i in range(len(train)):
  if i % 2 == 0:
    away1.append(i)
  else:
    home1.append(i)

away=train.loc[away1]
away=away.reset_index(drop=True)
home=train.loc[home1]
home=home.reset_index(drop=True)

train=away.subtract(home)
train['Result']=away['Result']

train=train.astype(float)
print(train.corr()['Result'])

Y=train.pop('Result')
X=train

clf=LinearRegression(n_jobs=-1)

clf.fit(X,Y)

# split data into train and test sets
accs=[]
for rs in range(100):
	x_train,x_test,y_train,y_test = train_test_split(X, Y, test_size=0.2, random_state=rs)

	preds=list(clf.predict(x_test))
	#print(preds[:5])
	accs.append(f.myacc(preds,y_test))

	#print(f.myacc(preds,y_test))
print(sum(accs)/len(accs))
#joblib.dump(clf,'sum_subtract')

x_train = torch.Tensor(x_train.values)
x_test = torch.Tensor(x_test.values)

y_train = torch.Tensor(y_train.values)
y_test= torch.Tensor(y_test.values)
y_train=y_train.unsqueeze(1)

model = torch.nn.Sequential(
    torch.nn.Linear(len(train.columns), len(train.columns)),
    torch.nn.Sigmoid(),
    torch.nn.Linear(len(train.columns), len(train.columns)),
    torch.nn.Sigmoid(),
    torch.nn.Linear(len(train.columns),1),
)
loss_fn = torch.nn.MSELoss()

learning_rate = 4e-4
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

max=0
for t in range(1000):
	y_pred = model(x_train)
	loss = loss_fn(y_pred, y_train)
	preds = model(x_test)
	acc=f.myacc(preds,y_test)
	if acc > max:
		print('saved',acc)
		torch.save(model,'players_model68')
		max=acc
	if t % 30 == 0:
		print(t, loss.item(), f.myacc(y_pred,y_train))
	#f.myacc(y_pred,y_train))

	optimizer.zero_grad()

	loss.backward()

	optimizer.step()

print('train:',f.myacc(model(x_train),y_train),'test:',f.myacc(preds,y_test))
#torch.save(model,'./123')


