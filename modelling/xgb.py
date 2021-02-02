import pandas as pd
import functions as f
import xgboost as xgb
from sklearn.model_selection import train_test_split
import joblib

# load data
#train_name='../data/data25wr.csv'
train_name='../data/train20.csv'
train=pd.read_csv(train_name)
print('using '+train_name)

test=train.loc[train['date'] < 20200000]
test=test.loc[train['date'] > 20180000]
train=train.drop(test.index)
train=train.drop(['home','away','date'],1)
test=test.drop(['home','away','date'],1)
#print(train.corr()['result'])

nans=train[train.isnull().T.any().T]
print(nans.index)

y_train=train.pop('result')
x_train=train.values

y_test=test.pop('result')
x_test=test.values

#Y=train.pop('result')
#X=train

# fit model no training data
clf= xgb.XGBRegressor()

#X=X.values
#Y=Y.values

#x_train,x_test,y_train,y_test = train_test_split(X, Y, test_size=0.2, random_state=1)

clf.fit(x_train,y_train)

# split data into train and test sets
"""
accs=[]
for rs in range(100):
	x_train,x_test,y_train,y_test = train_test_split(X, Y, test_size=0.2, random_state=rs)
	preds=list(clf.predict(x_test))
	accs.append(f.myacc(preds,y_test))
"""
preds=list(clf.predict(x_test))
print(f.myacc(preds,y_test))
"""
print(preds[:5])
print('acc on 100 different test sets is:',sum(accs)/len(accs))
"""
if input('want to dump model? (y or n) ') == 'y':
	joblib.dump(clf,input('name of file to dump on '))

