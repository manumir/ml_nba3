import pandas as pd
import functions as f
from sklearn.linear_model import LinearRegression
import joblib

# load data
#train_name='../data/data25wr.csv'
train_name='../data/train60.csv'
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

# fit model no training data
#clf= xgb.XGBRegressor()
clf= LinearRegression()

clf.fit(x_train,y_train)

# split data into train and test sets
preds=list(clf.predict(x_test))
print(f.myacc(preds,y_test))

if input('want to dump model? (y or n) ') == 'y':
	joblib.dump(clf,input('name of file to dump on '))

