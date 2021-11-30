def op():
    global driver,s,v,timestamp,tempoFrente, ca, ve
    co = driver.find_element_by_id("dt_purchase_put_button")
    ve = driver.find_element_by_id("dt_purchase_call_button")
    timestamp = 5
    tempoFrente = 5

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
            co.click()
        else:
            ve.click()
