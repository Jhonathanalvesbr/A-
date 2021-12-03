import undetected_chromedriver as uc
import pandas as pd
import numpy as np
from keras.layers import Dropout
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
from sklearn.preprocessing import MinMaxScaler
import math
import matplotlib.pyplot as plt
import os
from selenium.webdriver.common.by import By
import time
import random
import pymysql
from selenium.webdriver.common.keys import Keys
import copy
from datetime import datetime
import numpy
import treinamento
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

def getVetor():
    global tempoFrente
    global timestamp
    global v
    v = []
    conexao = pymysql.connect(db='deriv', user='root', passwd='root')
    cursor = conexao.cursor()
    cursor.execute("select valor from preco where id%5 == 0 ORDER BY id desc LIMIT "+str(timestamp-tempoFrente)+";")
    tmp = cursor.fetchall()
    for k in tmp:
        v.append([float(str(k).replace("(","").replace(")","").replace(",",""))])
        
def c():
    global driver
    global model
    global sc, conexao, tmp, cursor
    valor  = float(driver.find_elements_by_class_name("cq-current-price")[0].text)
    v = float(sc.inverse_transform(model.predict([[[float(model.predict([[[sc.fit_transform([[valor]])[0][0]]]])[0][0][0])]]])[0])[0][0])
    valor  = float(driver.find_elements_by_class_name("cq-current-price")[0].text)
    qnt = 5
    while qnt > 0:
        vv()
        qnt -= 1
        r = random.randint(10,15)
        
        if(v > valor):
            driver.find_elements_by_id("dt_purchase_call_button")[0].click()
        else:
            driver.find_elements_by_id("dt_purchase_put_button")[0].click()
        try:
            driver.find_elements_by_class_name("stx-subholder")[0].click()
        except:
            time.sleep(0.1)
            driver.find_elements_by_class_name("stx-subholder")[0].click()
        time.sleep(r)


def cc():
    global driver
    global regressor
    global sc

    vv()
    v = []
    aux = float(driver.find_elements_by_class_name("cq-current-price")[0].text)
    v.append(aux)
    while len(v) < timestamp:
        aux = float(driver.find_elements_by_class_name("cq-current-price")[0].text)
        if(v[len(v)-1] != aux):
            v.append(aux)
        
    v = np.array(v)
    v = v.reshape(-1,1)
    v = sc.transform(v)
    v = np.array([v])
    v = regressor.predict(v)
    v = sc.inverse_transform(v)



    valor  = float(driver.find_elements_by_class_name("cq-current-price")[0].text)

    if(v < valor):
        driver.find_elements_by_id("dt_purchase_call_button")[0].click()
    else:
        driver.find_elements_by_id("dt_purchase_put_button")[0].click()
    driver.find_elements_by_class_name("stx-subholder")[0].click()

def vv():
    global driver
    global val
    global win
    global loss
    global r
    global lot
    
    v = float((driver.find_elements_by_class_name("acc-info__account-type-and-balance")[0].text.replace(" USD", "")).split(".")[0].replace(",",""))
    try:
        if(val > 9):
            val = 1
        if("Lost" == driver.find_elements_by_class_name("dc-contract-card__wrapper")[0].text.split("\n")[0]):
            loss += 1
            val *= 1.5
            if(val == 0):
                val = 1
            r = 10
            lot += 1
            while(driver.find_element_by_id("dt_amount_input").get_attribute("value") > ''):
                driver.find_element_by_id("dt_amount_input").send_keys(Keys.BACKSPACE)
            driver.find_element_by_id("dt_amount_input").send_keys(round(((v)/100)*val,2))
        else:
            win += 1
            lot = 0
            val = 1
            while(driver.find_element_by_id("dt_amount_input").get_attribute("value") > ''):
                driver.find_element_by_id("dt_amount_input").send_keys(Keys.BACKSPACE)
            driver.find_element_by_id("dt_amount_input").send_keys(round(((v)/100)*val,2))
        
    except:
        return
        
def p():
	global dados
	k = []
	j = 0
	for x in dados:
		k.append(j)
		j+= 1
	d = []
	i = 0
	#while i < 0:
#		d.append(float(sc.inverse_transform(model.predict([[[float(model.predict([[[sc.fit_transform([dados[0]])[0][0]]]])[0][0][0])]]])[0])[0][0]))
#		i += 1
	while i < len(dados):
		d.append(float(sc.inverse_transform(model.predict([[[float(model.predict([[[sc.fit_transform([dados[i]])[0][0]]]])[0][0][0])]]])[0])[0][0]))
		i+= 1
	
	print(len(d))
	plt.plot(k, dados, label = "line 1", color="green")
	plt.plot(k, d, label = "line 2", color="red")
	plt.show()





def train():
    #time.sleep(1)
    global dados
    global model
    global sc
    global win
    global loss
    print("Win: " +  str(win) + " - Loss: " +str(loss) )
    
    getValor()
    sc = MinMaxScaler(feature_range = (0,1))
    dados = dados[:250]
    training_set_scaled = sc.fit_transform(dados)
    x_train = []
    y_train = []
    timestamp = 5
    length = len(dados)
    for i in range(timestamp, length):
            x_train.append(training_set_scaled[i-timestamp:i,0])
            y_train.append(training_set_scaled[i,0])
    x_train = np.array(x_train)
    y_train = np.array(y_train)
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1],1))
    model = Sequential()
    model.add(LSTM(units = 50, return_sequences = True, input_shape = (x_train.shape[1],1)))
    model.add(Dropout(0.2))
    model.add(LSTM(units = 50, return_sequences = True))
    model.add(Dropout(0.2))
    model.add(LSTM(units = 50, return_sequences = True))
    model.add(Dropout(0.2))
    model.add(LSTM(units = 50))
    model.add(Dropout(0.2))
    
    model.add(Dense(units=1))
    model.compile(optimizer = 'adam', loss = 'mean_squared_error')
    model.fit(x_train, y_train, epochs = 100, batch_size = 32, verbose= 2)
    #getValor()

    c()


regressor = ""
X_test = ""
sc = ""
lot = 0

def getValor():
    global dados
    global dado
    dados = []
    dado = []
    conexao = pymysql.connect(db='deriv', user='root', passwd='root')
    cursor = conexao.cursor()
    r = random.randint(10,20)
    cursor.execute("select valor from preco ORDER BY id desc LIMIT 1800;")
    #cursor.execute("select valor,segundos,milisegundos from preco WHERE MOD(id, "+str(r)+") = 0 ORDER BY id desc LIMIT 2000;")
    tmp = cursor.fetchall()
    #for k in tmp:
    #    dados.append([eval(x) for x  in str(k).replace("(","").replace(")", "").split(",")[:4]])
    #dados = list(reversed(dados))
    for k in tmp:
        dados.append([float(str(k).replace("(","").replace(")","").replace(",",""))])
        #dado.append(float(str(k).replace("(","").replace(")","").replace(",","")))
    #dados = list(reversed(dados))

def treinar():
    global a
    global b
    global c
    global d
    global e
    global aux
    global v
    a = treinamento.treinamento(25,7,"adam","mean_squared_error",1500)
    a.treinar()
    b = treinamento.treinamento(25,7,"adam","mean_squared_error",1200)
    b.treinar()
    c = treinamento.treinamento(25,7,"adam","mean_squared_error",900)
    c.treinar()
    d = treinamento.treinamento(25,7,"adam","mean_squared_error",600)
    d.treinar()
    e = treinamento.treinamento(25,7,"adam","mean_squared_error",300)
    e.treinar()
   

    
def predizer():
    global a
    global b
    global c
    global d
    global e
    global v
    
    v1 = sc.inverse_transform(a.regressor.predict(v))[0][0]
    v2 = sc.inverse_transform(b.regressor.predict(v))[0][0]
    v3 = sc.inverse_transform(c.regressor.predict(v))[0][0]
    v4 = sc.inverse_transform(d.regressor.predict(v))[0][0]
    v5 = sc.inverse_transform(e.regressor.predict(v))[0][0]

    return [v1, v2, v3, v4, v5]
 
def tt():
    global dados
    global regressor
    global x
    global y
    global sc
    global v
    global win
    global loss
    global lot
    global val
    global x
    global tempoFrente
    global timestamp
    
    print("Win: " +  str(win) + " - Loss: " +str(loss) )
    getValor()
    #dados = converter(dados)
    training_set = dados
    #training_set = dados[:250]
    real_stock_price = copy.deepcopy(training_set)
    sc = MinMaxScaler(feature_range = (0, 1))
    training_set_scaled = sc.fit_transform(training_set)
    length = len(training_set)
    
    timestamp -= tempoFrente
    x = []
    y = []
    for i in range(timestamp, length):
        x.append(training_set_scaled[i-timestamp:i-tempoFrente])
        #soma = sum(training_set_scaled[i-timestamp:i])/len(x)
        #x[len(x)-1] = numpy.append(x[len(x)-1], soma)
        #x[len(x)-1] = np.append([x[len(x)-1].tolist()[0]], [soma.tolist()], axis=0)
        #o = x[len(x)-1].tolist()
        #o.append(soma.tolist())
        #x[len(x)-1] = np.array(o)
        y.append(training_set_scaled[i])
    x, y = np.array(x), np.array(y)

    x = np.reshape(x, (x.shape[0], x.shape[1], len(dados[0])))

    regressor = Sequential()

    regressor.add(LSTM(units = 120, return_sequences = True, input_shape = (x.shape[1], len(dados[0]))))
    regressor.add(Dropout(0.2))

    regressor.add(LSTM(units = 120, return_sequences = True))
    regressor.add(Dropout(0.2))
    regressor.add(LSTM(units = 120, return_sequences = True))
    regressor.add(Dropout(0.2))


    regressor.add(LSTM(units = 120, return_sequences = False))
    regressor.add(Dropout(0.2))

    regressor.add(Dense(units = 1))

    regressor.compile(optimizer = 'adam', loss = 'log_cosh')

    regressor.fit(x, y, epochs = 25, batch_size = 32, verbose= 2)
    contadorErro = 0

    while lot < 2:
        driver.find_elements_by_class_name("stx-subholder")[0].click()
        v = []
        vv()
        try:
            print("Win: " +  str(win) + " - Loss: " +str(loss) )
            if(lot == 2):
                lot = -1
                val = 0
                return
            operacao()
            contadorErro += 1
            #time.sleep(1)
            
        except:
            time.sleep(0.1)
            print("Win: " +  str(win) + " - Loss: " +str(loss) )
            if("Won" == driver.find_elements_by_class_name("dc-contract-card__wrapper")[0].text.split("\n")[0]):
                lot = -1
                val = 0
            v = []
        time.sleep(5)
        driver.find_elements_by_class_name("stx-subholder")[0].click()
        if("Lost" == driver.find_elements_by_class_name("dc-contract-card__wrapper")[0].text.split("\n")[0]):
            lot = -2
            val = 0
            return
    lot = -2
    val = 0
                
    
def compraVenda():
    global dados
    global regressor
    global x
    global y
    global sc
    global v
    global win
    global loss
    global lot
    global val
    global x
    global tempoFrente
    global timestamp
    global a
    global b
    global c
    global d
    global e
    global valor
    
    treinar()
    tmp()

def tmp():
    global lot
    global val
    global driver
    while(True):
        while lot < 2:
            driver.find_elements_by_class_name("stx-subholder")[0].click()
            v = []
            vv()
            try:
                print("Win: " +  str(win) + " - Loss: " +str(loss) )
                if(lot == 2):
                    lot = -1
                    val = 0
                    return
                operacao()
                t = todos()
                aux = valor
                print(aux)
                print(t)
                if(aux < t[0] and aux < t[1] and aux < t[2] and aux <  t[3] and aux < t[4]):
                    #driver.find_elements_by_id("dt_purchase_put_button")[0].click()
                
                    driver.find_elements_by_id("dt_purchase_call_button")[0].click()    
                elif(aux > t[0] and aux > t[1] and aux > t[2] and aux >  t[3] and aux > t[4]):
                    #driver.find_elements_by_id("dt_purchase_call_button")[0].click()

                    driver.find_elements_by_id("dt_purchase_put_button")[0].click()
                else:
                    lot = -2
                    val = 0
                contadorErro += 1
                #time.sleep(1)
                
            except:
                time.sleep(0.1)
                print("Win: " +  str(win) + " - Loss: " +str(loss) )
                if("Won" == driver.find_elements_by_class_name("dc-contract-card__wrapper")[0].text.split("\n")[0]):
                    lot = -1
                    val = 0
                v = []
            time.sleep(5)
            driver.find_elements_by_class_name("stx-subholder")[0].click()
        lot = -2
        val = 0
        return
    '''inputs = dados[:250]
    inputs = np.array(inputs)
    inputs = inputs.reshape(-1,1)
    inputs = sc.transform(inputs)
    X_test = []
    for i in range(timestamp, length):
        X_test.append(inputs[i-timestamp:i, 0])
    X_test = np.array(X_test)
    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
    predicted_stock_price = regressor.predict(X_test)
    predicted_stock_price = sc.inverse_transform(predicted_stock_price)

    plt.plot(real_stock_price, color = 'green', label = 'TATA Stock Price')
    plt.plot(predicted_stock_price, color = 'red', label = 'Predicted TATA Stock Price')
    plt.title('TATA Stock Price Prediction')
    plt.xlabel('Time')
    plt.ylabel('TATA Stock Price')
    plt.legend()
    plt.show()
    '''


def operacao():
            global driver
            global v
            global aux
            global tempo
            global regressor
            global time
            global timestamp
            global tempoFrente
            global sc
            global valor
            
            getVetor()
            valor = v[0][0]
            #v = [v]
            #v = np.array(v)
            #v = v.reshape(-1,1)
            #v = converter(v)
            sc = MinMaxScaler(feature_range = (0, 1))
            v = sc.fit_transform(v)
            #soma = sum(v)/len(v)
            #o = v.tolist()
            #o.append(soma.tolist())
            #v = np.array(o)
            v = np.array([v])
            #print(v)
            return
            v = regressor.predict(v)
            v = sc.inverse_transform(v)
            
            #print(v[0][0])
            #if((min(dados)[0] < aux < max(dados)[0]) == False):
            if(True == False):
                return
            else:
                print("Valor: " + str(aux))
                print("Previ: " + str(v[0][0]))
                #if(v[0][0] > 0):
                if(v[0][0] > valor):
                    driver.find_elements_by_id("dt_purchase_call_button")[0].click()
                    v = []
                else:
                    driver.find_elements_by_id("dt_purchase_put_button")[0].click()
                    v = []
                time.sleep(10)
                #time.sleep(3)
                #print(v)
                v = []

def converter(dados):
    d = []

    k = 0;

    while(k < len(dados)-1):
        if(dados[k][0] < dados[k+1][0]):
            d.append([1])
        else:
            d.append([-1])
        k += 1
    return d
    



def t():
    global dados
    global sc
    global np
    global model
    
    a = dados[:250]
    v = copy.deepcopy(a)
    a = np.array(a)
    a = sc.transform(a)
    timestamp = 5
    length = len(a)
    for i in range(timestamp, length):
                x_teste.append(a[i-timestamp:i,0])
    a = np.array(a)
    a = np.reshape(a, (a.shape[0], a.shape[1],1))
    pred = model.predict(a)
    pre = sc.inverse_transform(pred)
    plt.plot(v, color = "black")
    plt.plot(pre)
    plt.show()
    


def getNewValor():
    global dados
    dados = []
    conexao = pymysql.connect(db='deriv', user='root', passwd='root')
    cursor = conexao.cursor()
    cursor.execute("select valor from preco ORDER BY id desc LIMIT 1000;")
    tmp = cursor.fetchall()
    for k in tmp:
        dados.append([float(str(k).replace("(","").replace(")","").replace(",",""))])
    dados = list(reversed(dados))
    
        
driver = uc.Chrome()
driver.get('https://app.deriv.com/')
ganho = True
aux = None
r = None
model  = None
sc = None
val = 1
dados = []
time.sleep(5)
ini = time.time()
fim = time.time()
r = random.randint(10,20)
win = 0
loss  = 0
#driver.switch_to.window(driver.window_handles[0])

def atualizar():
    global driver
    global win
    global loss
    global martingale
    banca = float((driver.find_elements_by_class_name("acc-info__account-type-and-balance")[0].text.replace(" USD", "")).split(".")[0].replace(",",""))

    if("Lost" == driver.find_elements_by_class_name("dc-contract-card__wrapper")[0].text.split("\n")[0]):
        loss += 1
        martingale *= 2
        #while(driver.find_element_by_id("dt_amount_input").get_attribute("value") > ''):
        #    driver.find_element_by_id("dt_amount_input").send_keys(Keys.BACKSPACE)
        #driver.find_element_by_id("dt_amount_input").send_keys(round(((banca)/10)*martingale,2))
    else:
        win += 1
        martingale = 1
        #while(driver.find_element_by_id("dt_amount_input").get_attribute("value") > ''):
        #    driver.find_element_by_id("dt_amount_input").send_keys(Keys.BACKSPACE)
        #driver.find_element_by_id("dt_amount_input").send_keys(round(((banca)/10)*martingale,2))

    

def getVetor():
    global tempoFrente
    global timestamp
    global v
    v = []
    conexao = pymysql.connect(db='deriv', user='root', passwd='root')
    cursor = conexao.cursor()
    cursor.execute("select valor from preco ORDER BY id desc LIMIT "+str(timestamp-tempoFrente)+";")
    tmp = cursor.fetchall()
    for k in tmp:
        v.append([float(str(k).replace("(","").replace(")","").replace(",",""))])

def treinar():
    global a
    global b
    global c
    global d
    global e
    global aux
    global v
    global timestamp
    global tempoFrente
    global random

    timestamp = random.randint(21,28)
    tempoFrente = random.randint(7,14)
    
    a = treinamento.treinamento(timestamp,tempoFrente,"adam","mean_squared_error",random.randint(120,600),"LSTM")
    a.treinar()
    b = treinamento.treinamento(timestamp,tempoFrente,"rmsprop","log_cosh",random.randint(120,600),"GRU")
    b.treinar()
    c = treinamento.treinamento(timestamp,tempoFrente,"adam","huber_loss",random.randint(120,600),"GRU")
    c.treinar()
    d = treinamento.treinamento(timestamp,tempoFrente,"rmsprop","mean_squared_error",random.randint(120,600),"LSTM")
    d.treinar()
    e = treinamento.treinamento(timestamp,tempoFrente,"adam","log_cosh",random.randint(120,600),"")
    e.treinar()


def predizer():
    global a, b, c, d, e, v, p, martingale, win, loss, timestamp, tempoFrente, sc
    
    timestamp = 14
    tempoFrente = 7
    
    #treinar()
    ini = time.time()
    fim = time.time()
    r = 120
    p = []
    p.append(op())
    while(True):
        operacao = 0
        
        getVetor()
        
        #p.append(v[0][0])
        #v = sc.fit_transform(v)
        #v = np.array([v])

        #p.append(sc.inverse_transform(a.regressor.predict(v))[0][0])
        #p.append(sc.inverse_transform(b.regressor.predict(v))[0][0])
        #p.append(sc.inverse_transform(c.regressor.predict(v))[0][0])
        #p.append(sc.inverse_transform(d.regressor.predict(v))[0][0])
        #p.append(sc.inverse_transform(e.regressor.predict(v))[0][0])
        print(p,v[0])
        #if(p[0] >= max(v)):
        if(p[0] >= v[0]):
            driver.find_elements_by_id("dt_purchase_put_button")[0].click()
            #driver.find_elements_by_id("dt_purchase_call_button")[0].click()
            operacao = 1
        #elif(p[0] <= min(v)):
        elif(p[0] <= v[0]):
            driver.find_elements_by_id("dt_purchase_call_button")[0].click()
            #driver.find_elements_by_id("dt_purchase_put_button")[0].click()
            operacao =  1
        else:
            operacao = 0

        if(operacao == 1):
            print("Win : " + str(win))
            print("Loss: " + str(loss))
            time.sleep(7)
            atualizar()
            time.sleep(3)
        if(fim-ini > r):
            if("Lost" == driver.find_elements_by_class_name("dc-contract-card__wrapper")[0].text.split("\n")[0]):
                p = []
                p.append(op())
                #treinar()
                ini = time.time()
        if(martingale >= 8 and "Lost" == driver.find_elements_by_class_name("dc-contract-card__wrapper")[0].text.split("\n")[0]):
                p = []
                p.append(op())
                #treinar()
                ini = time.time()
        fim = time.time()


def predizer():
    global a, b, c, d, e, v, p, martingale, win, loss, timestamp, tempoFrente, sc
    
    timestamp = 14
    tempoFrente = 7
    
    treinar()
    ini = time.time()
    fim = time.time()
    r = 120
    while(True):
        operacao = 0
        
        getVetor()
        p = []
        p.append(v[0][0])
        v = sc.fit_transform(v)
        v = np.array([v])

        p.append(sc.inverse_transform(a.regressor.predict(v))[0][0])
        p.append(sc.inverse_transform(b.regressor.predict(v))[0][0])
        p.append(sc.inverse_transform(c.regressor.predict(v))[0][0])
        p.append(sc.inverse_transform(d.regressor.predict(v))[0][0])
        p.append(sc.inverse_transform(e.regressor.predict(v))[0][0])
        print(p)
        if(p[0] >= max(p)):
            driver.find_elements_by_id("dt_purchase_put_button")[0].click()
            #driver.find_elements_by_id("dt_purchase_call_button")[0].click()
            operacao = 1
        elif(p[0] <= min(p)):
            driver.find_elements_by_id("dt_purchase_call_button")[0].click()
            #driver.find_elements_by_id("dt_purchase_put_button")[0].click()
            operacao =  1
        else:
            operacao = 0

        if(operacao == 1):
            print("Win : " + str(win))
            print("Loss: " + str(loss))
            time.sleep(7)
            atualizar()
            time.sleep(3)
        if(fim-ini > r):
            if("Lost" == driver.find_elements_by_class_name("dc-contract-card__wrapper")[0].text.split("\n")[0]):
                treinar()
                ini = time.time()
        if(martingale >= 8 and "Lost" == driver.find_elements_by_class_name("dc-contract-card__wrapper")[0].text.split("\n")[0]):
                treinar()
                ini = time.time()
        fim = time.time()

def prep(data):
    k = []
    for i in data:
        k.append([i])

    return np.array(k).astype('float32')
    

def prepit(data, lags = 1):
    global timestamp,tempoFrente
    x, y = [], []
    for row in range(len(data) - lags - 1):
        a = data[row:(row + lags), 0]
        x.append(a)
        y.append(data[row + lags, 0])
    return np.array(x), np.array(y)
        

def prepare_data(data):
    global timestamp,tempoFrente
    x, y = [], []
    for i in range(timestamp, len(data)):
            x.append(training_set_scaled[i-timestamp:i-tempoFrente])
            y.append(training_set_scaled[i])
    return np.array(x).astype('float32'), np.array(y).astype('float32')

def prepare_data(data):
    global timestamp,tempoFrente
    x, y = [], []
    for i in range(timestamp, len(data)):
        a = data[i-timestamp:i-tempoFrente]
        #a = str(a.tolist()).replace("[","").replace("]","")
        #a = list(a.split(","))
        #a = [float(item) for item in t]
        x.append(a)
        y.append([data[i]])
    return np.array(x).astype('float32'), np.array(y).astype('float32')

def op():
    global dados, mdl, sc
    getValor()
    sc = MinMaxScaler(feature_range = (0,1))
    dado = sc.fit_transform(dados)
    dado = numpy.array(dados).flatten()
    x, y = prepare_data(dado)
    
    mdl = Sequential()
    mdl.add(Dense(12, input_dim=len(x[0]), activation='relu'))
    mdl.add(Dense(12, activation='relu'))
    mdl.add(Dense(3, activation='relu'))
    mdl.add(Dense(1))
    mdl.compile(loss='categorical_hinge', optimizer='adam')
    mdl.fit(x, y, epochs=50, batch_size=2, verbose=2)

    getVetor()
    tmp = v
    t = sc.fit_transform(v)
    pre = [numpy.array(t).flatten().tolist()]
    res = mdl.predict(pre)
    res = sc.inverse_transform(res)[0][0]
    return res

def op():
    global dados, mdl, sc, pre, tmp, v, dado
    while(True):
        getValor()
        sc = MinMaxScaler(feature_range = (-1,1))
        sc.fit_transform(dados)
        dado = numpy.array(dados).flatten()
        x, y = prepare_data(dado)
        
        mdl = Sequential()
        mdl.add(Dense(12, input_dim=len(x[0]), activation='relu'))
        mdl.add(Dense(12, activation='relu'))
        mdl.add(Dense(3, activation='relu'))
        mdl.add(Dense(1))
        mdl.compile(loss='categorical_hinge', optimizer='adam')
        #mdl.compile(loss='mean_squared_error', optimizer='adam')
        mdl.fit(x, y, epochs=50, batch_size=2, verbose=2)

        getVetor()
        tmp = v
        t = sc.fit_transform(v)
        pre = [numpy.array(t).flatten().tolist()]
        pre = [numpy.array(v).flatten().tolist()]
        res = mdl.predict(pre)
        res = sc.inverse_transform(res)[0][0]
        a = res
        b = dados[timestamp][0]
        porcent = (a*100)/b
        print(porcent)
        if(90 < porcent < 110):
            break
    return res
                    
timestamp = 14
tempoFrente = 7

def op():
    global driver
    global ini
    global fim
    global r
    global aux
    global timestamp
    global tempoFrente
    
    timestamp = 14
    tempoFrente = 7
    while True:
        valor  = float(driver.find_elements_by_class_name("cq-current-price")[0].text)
        if(aux != valor):
            aux = valor
        if(fim-ini > r):
            try:
                driver.find_elements_by_class_name("stx-subholder")[0].click()
                #driver.get('https://app.deriv.com/')
                #tt()
                compraVenda()
                r = 0
                #train()
                    #r = random.randint(30,60)
                    #ini = time.time()
            except:
                r = random.randint(1,10)
                ini = time.time()
            #r = random.randint(10,20)
            ini = time.time()
        fim = time.time()



































# univariate multi-step vector-output stacked lstm example


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
    global s,tempo
    v = []
    conexao = pymysql.connect(db='deriv', user='root', passwd='root')
    cursor = conexao.cursor()
    cursor.execute("select valor from preco WHERE id%"+str(tempo)+" = 0 ORDER BY id desc LIMIT "+str(timestamp)+";")
    tmp = cursor.fetchall()
    for k in tmp:
        v.append(float(str(k).replace("(","").replace(")","").replace(",","")))
    s = v[::-1]
    #v = v[0:100]

def getVetorAnterior():
    global tempoFrente
    global timestamp
    global sAnterior,tempo
    v = []
    conexao = pymysql.connect(db='deriv', user='root', passwd='root')
    cursor = conexao.cursor()
    cursor.execute("select valor from preco WHERE id%"+str(tempo)+" = 0 ORDER BY id desc LIMIT "+str(timestamp+1)+";")
    tmp = cursor.fetchall()
    for k in tmp:
        v.append(float(str(k).replace("(","").replace(")","").replace(",","")))

    v.pop(0)
    sAnterior = v[::-1]
    #v = v[0:100]

def getDados():
    global tempoFrente
    global timestamp
    global v,s,tempo
    v = []
    conexao = pymysql.connect(db='deriv', user='root', passwd='root')
    cursor = conexao.cursor()
    cursor.execute("select valor from preco WHERE id%"+str(tempo)+" = 0 ORDER BY id desc LIMIT "+str(100)+";")
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



martingale = 1
def op():
    global driver,s,v,timestamp, tempoFrente, cO, ve, win, loss, cursor, conexao
    global sAnterior,tempo
    tempo = 8
    win = 1
    loss = 1
    timestamp = 2
    tempoFrente = 1
    driver.switch_to.window(driver.window_handles[0])
    co = driver.find_element(By.ID,"dt_purchase_put_button")
    ve = driver.find_element(By.ID,"dt_purchase_call_button")
    while(True):
        
        
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
        model.add(LSTM(120, activation='LeakyReLU', return_sequences=True, input_shape=(n_steps_in, n_features)))
        model.add(LSTM(120, activation='LeakyReLU', return_sequences=True))
        model.add(LSTM(120, activation='LeakyReLU', return_sequences=False))
        model.add(Dense(n_steps_out))
        model.compile(optimizer='Adadelta', loss='mse')
        # fit model
        model.fit(X, y, epochs = 100, batch_size = 32, verbose=0)
        # demonstrate prediction
        #x_input = array([[5822.11],[5822.45],[5823.75],[5825.37],[5824.63],[5825.15]])

        #x_input = sc.fit_transform(x_input)
        #x_input = numpy.array(x_input).flatten().tolist()

        #x_input = x_input.reshape((1, n_steps_in, n_features))
        #yhat = model.predict(X, verbose=0)
        #yhat = sc.inverse_transform(yhat)
        #values = [np.nan]*(tempoFrente)
        #values = np.append(values, y)
        #values.reshape(values.shape[0], 1)
        #y = sc.inverse_transform(y)
        #plt.plot(s, color = "black")
        #plt.plot(v, color = "blue", alpha=.5)

        #plt.plot(values, color = "green")
        #plt.plot(yhat, color = "red")
        #plt.show()

        conexao = pymysql.connect(db='deriv', user='root', passwd='root')
        cursor = conexao.cursor()
        cursor.execute("select id from preco ORDER BY id desc LIMIT "+str(1)+";")
        tmp = cursor.fetchall()
        tmp = int(str(tmp).replace("(","").replace(")","").replace(",",""))
        tmp = tmp %tempo
        while(tmp != 0):
            conexao = pymysql.connect(db='deriv', user='root', passwd='root')
            cursor = conexao.cursor()
            cursor.execute("select id from preco ORDER BY id desc LIMIT "+str(1)+";")
            tmp = cursor.fetchall()
            tmp = int(str(tmp).replace("(","").replace(")","").replace(",",""))
            tmp = tmp %tempo
                
        getVetor()
        getVetorAnterior()
        a = s
        a = np.array(a)
        a = a.reshape(-1,1)
        a = np.array([a])
        a = model.predict(a)
        a = a[0][0]
            
        aa = sAnterior
        aa = np.array(aa)
        aa = aa.reshape(-1,1)
        aa = np.array([aa])
        aa = model.predict(aa)
        aa = aa[0][0]
            
        atualizar()
        valor  = float(driver.find_elements_by_class_name("cq-current-price")[0].text)
        print([valor,a, win, loss, round((win*100)/(win+loss),2), round((loss*100)/(win+loss),2)])
        if(aa < a):
                co.click()
        else:
                ve.click()
        
        time.sleep(11)
        
        





'''
def op():
    global driver,s,v,timestamp, tempoFrente, cO, ve, win, loss, cursor, conexao
    global sAnterior
    win = 1
    loss = 1
    timestamp = 2
    tempoFrente = 1
    driver.switch_to.window(driver.window_handles[0])
    co = driver.find_element(By.ID,"dt_purchase_put_button")
    ve = driver.find_element(By.ID,"dt_purchase_call_button")
    while(True):


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
        model.add(LSTM(120, activation='LeakyReLU', return_sequences=True, input_shape=(n_steps_in, n_features)))
        model.add(LSTM(120, activation='LeakyReLU', return_sequences=True))
        model.add(LSTM(120, activation='LeakyReLU', return_sequences=False))
        model.add(Dense(n_steps_out))
        model.compile(optimizer='Adadelta', loss='mse')
        # fit model
        model.fit(X, y, epochs = 100, batch_size = 32, verbose=0)
        # demonstrate prediction
        #x_input = array([[5822.11],[5822.45],[5823.75],[5825.37],[5824.63],[5825.15]])

        #x_input = sc.fit_transform(x_input)
        #x_input = numpy.array(x_input).flatten().tolist()

        #x_input = x_input.reshape((1, n_steps_in, n_features))
        #yhat = model.predict(X, verbose=0)
        #yhat = sc.inverse_transform(yhat)
        #values = [np.nan]*(tempoFrente)
        #values = np.append(values, y)
        #values.reshape(values.shape[0], 1)
        #y = sc.inverse_transform(y)
        #plt.plot(s, color = "black")
        #plt.plot(v, color = "blue", alpha=.5)

        #plt.plot(values, color = "green")
        #plt.plot(yhat, color = "red")
        #plt.show()

        conexao = pymysql.connect(db='deriv', user='root', passwd='root')
        cursor = conexao.cursor()
        cursor.execute("select id from preco ORDER BY id desc LIMIT "+str(1)+";")
        tmp = cursor.fetchall()
        tmp = int(str(tmp).replace("(","").replace(")","").replace(",",""))
        tmp = tmp %13
        while(tmp != 0):
                conexao = pymysql.connect(db='deriv', user='root', passwd='root')
                cursor = conexao.cursor()
                cursor.execute("select id from preco ORDER BY id desc LIMIT "+str(1)+";")
                tmp = cursor.fetchall()
                tmp = int(str(tmp).replace("(","").replace(")","").replace(",",""))
                tmp = tmp %13

        getVetor()
        getVetorAnterior()
        a = s
        a = np.array(a)
        a = a.reshape(-1,1)
        a = np.array([a])
        a = model.predict(a)
        a = a[0][0]

        aa = sAnterior
        aa = np.array(aa)
        aa = aa.reshape(-1,1)
        aa = np.array([aa])
        aa = model.predict(aa)
        aa = aa[0][0]


        valor  = float(driver.find_elements_by_class_name("cq-current-price")[0].text)
        print([valor,a, win, loss, round((win*100)/(win+loss),2), round((loss*100)/(win+loss),2)])
        if(aa > a):
                co.click()
        else:
                ve.click()
        time.sleep(1)
        conexao = pymysql.connect(db='deriv', user='root', passwd='root')
        cursor = conexao.cursor()
        cursor.execute("select id from preco ORDER BY id desc LIMIT "+str(1)+";")
        tmp = cursor.fetchall()
        tmp = int(str(tmp).replace("(","").replace(")","").replace(",",""))
        tmp = tmp %13
        while(tmp != 0):
                conexao = pymysql.connect(db='deriv', user='root', passwd='root')
                cursor = conexao.cursor()
                cursor.execute("select id from preco ORDER BY id desc LIMIT "+str(1)+";")
                tmp = cursor.fetchall()
                tmp = int(str(tmp).replace("(","").replace(")","").replace(",",""))
                tmp = tmp %13
        atualizar()
'''
            
