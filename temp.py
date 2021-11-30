# univariate multi-step vector-output stacked lstm example
from numpy import array
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense
import pymysql
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
import numpy
import pandas as pd
import numpy as np
from keras.layers import Dropout

# split a univariate sequence into samples
def split(sequence, n_steps_in, n_steps_out):
	global tempoFrente
	X, y = list(), list()
	for i in range(len(sequence)-tempoFrente-1):
		# find the end of this pattern
		end_ix = i + n_steps_in
		out_end_ix = end_ix + n_steps_out
		# check if we are beyond the sequence
		if out_end_ix > len(sequence):
			break
		# gather input and output parts of the pattern
		seq_x, seq_y = sequence[i:end_ix], sequence[i+(tempoFrente+1)]
		X.append(seq_x)
		y.append([seq_y])
	return array(X), array(y)
    

def getVetor():
    global tempoFrente
    global timestamp
    global s
    v = []
    conexao = pymysql.connect(db='deriv', user='root', passwd='root')
    cursor = conexao.cursor()
    cursor.execute("select valor from preco ORDER BY id desc LIMIT "+str(timestamp)+";")
    tmp = cursor.fetchall()
    for k in tmp:
        v.append(float(str(k).replace("(","").replace(")","").replace(",","")))
    s = v[::-1]
    #v = v[0:100]

def getDados():
    global tempoFrente
    global timestamp
    global v,s
    v = []
    conexao = pymysql.connect(db='deriv', user='root', passwd='root')
    cursor = conexao.cursor()
    cursor.execute("select valor from preco ORDER BY id desc LIMIT "+str(100)+";")
    tmp = cursor.fetchall()
    for k in tmp:
        v.append(float(str(k).replace("(","").replace(")","").replace(",","")))
    v = v[::-1]
    #v = v[0:100]

def split_sequence(sequence, n_steps_in, n_steps_out):
	X, y = list(), list()
	for i in range(len(sequence)):
		# find the end of this pattern
		end_ix = i + n_steps_in
		out_end_ix = end_ix + n_steps_out
		# check if we are beyond the sequence
		if out_end_ix > len(sequence):
			break
		# gather input and output parts of the pattern
		seq_x, seq_y = sequence[i:end_ix], sequence[end_ix:out_end_ix]
		X.append(seq_x)
		y.append(seq_y)
	return array(X), array(y)


timestamp = 5
tempoFrente = 5


getDados()
'''
sc = MinMaxScaler(feature_range = (0, 1))
v = sc.fit_transform(v)
v = numpy.array(v).flatten().tolist()
'''
# define input sequence
raw_seq = v
# choose a number of time steps
n_steps_in, n_steps_out = timestamp, 1
# split into samples
X, y = split(raw_seq, n_steps_in, n_steps_out)
x = X

#print([x[0],y[0]])
#exit()
# reshape from [samples, timesteps] into [samples, timesteps, features]
n_features = 1
X = X.reshape((X.shape[0], X.shape[1], n_features))
# define model
model = Sequential()
model.add(LSTM(120, activation='relu', return_sequences=True, input_shape=(n_steps_in, n_features)))
model.add(LSTM(120, activation='relu', return_sequences=True))
model.add(LSTM(120, activation='relu', return_sequences=True))
model.add(LSTM(120, activation='relu', return_sequences=True))
model.add(LSTM(120, activation='relu', return_sequences=False))
model.add(Dense(n_steps_out))
model.compile(optimizer='adam', loss='mse')
# fit model
model.fit(X, y, epochs = 100, batch_size = 32, verbose=0)
# demonstrate prediction
#x_input = array([[5822.11],[5822.45],[5823.75],[5825.37],[5824.63],[5825.15]])

#x_input = sc.fit_transform(x_input)
#x_input = numpy.array(x_input).flatten().tolist()

#x_input = x_input.reshape((1, n_steps_in, n_features))
yhat = model.predict(X, verbose=0)
#yhat = sc.inverse_transform(yhat)
values = [np.nan]*(tempoFrente)
values = np.append(values, y)
values.reshape(values.shape[0], 1)
#y = sc.inverse_transform(y)
#plt.plot(s, color = "black")
#plt.plot(v, color = "blue", alpha=.5)

#plt.plot(values, color = "green")
#plt.plot(yhat, color = "red")
#plt.show()
getVetor()
a = s
a = np.array(a)
a = a.reshape(-1,1)
a = np.array([a])
a = model.predict(a)
a = a[0][0]
print([s[timestamp-1],a])

if(a < s[timestamp-1]):
    driver.find_elements_by_id("dt_purchase_call_button")[0].click()
else:
    driver.find_elements_by_id("dt_purchase_put_button")[0].click()
time.sleep(10)
