import pandas as pd
import functions as f 
from sklearn.model_selection import train_test_split
import torch

train_name='../data/train.csv'
train=pd.read_csv(train_name)
print('using',train_name)

train=train.drop(['home','away','date'],1)
#print(train.corr()['Result'])

nans=(train[train.isnull().T.any().T])
print(nans)

Y=train.pop('result')
X=train

x_train,x_test,y_train,y_test = train_test_split(X, Y, test_size=0.2, random_state=1)

x_train = torch.Tensor(x_train.values)
x_test = torch.Tensor(x_test.values)

y_train = torch.Tensor(y_train.values)
y_test= torch.Tensor(y_test.values)
y_train=y_train.unsqueeze(1)

model = torch.nn.Sequential(
    torch.nn.Linear(len(train.columns), len(train.columns)),
    torch.nn.Sigmoid(),
    torch.nn.Linear(len(train.columns),1),
)
loss_fn = torch.nn.MSELoss()

learning_rate = 3e-4
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

model_name2save=input('name of file to save model')
max=0
for t in range(2500):
	y_pred = model(x_train)
	loss = loss_fn(y_pred, y_train)
	preds = model(x_test)
	acc=f.myacc(preds,y_test)
	if acc > max:
		torch.save(model,model_name2save)
		max=acc
		print('saved')
	print(t, acc, loss.item())

	optimizer.zero_grad()

	loss.backward()

	optimizer.step()

print('train:',f.myacc(model(x_train),y_train),'test:',f.myacc(preds,y_test))
#torch.save(model,'./123')

model=torch.load('model_nn')

X=torch.Tensor(X.values)
preds=list(model(X))

print(f.myacc(preds,Y))


