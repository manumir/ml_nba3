import pandas as pd
import functions as f 
from sklearn.model_selection import train_test_split
import torch

train_name='../data/data40wr.csv'
train_name='../data/train20.csv'
train=pd.read_csv(train_name)
print('using',train_name)

train=train.drop(['home','away','date'],1)
#print(train.corr()['result'])

nans=(train[train.isnull().T.any().T])
print(nans.index)
train=train.drop(nans.index)

Y=train.pop('result')
X=train

model=torch.load(input('model name: '))

accs=[]
for rs in range(100):
	x_train,x_test,y_train,y_test = train_test_split(X, Y, test_size=0.2, random_state=rs)
	x_test=torch.Tensor(x_test.values)
	preds=list(model(x_test))
	accs.append(f.myacc(preds,y_test))

	#print(f.myacc(preds,y_test))
print(preds[:5])
print('acc on 100 different test sets is:',sum(accs)/len(accs))

