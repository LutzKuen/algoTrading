import datetime
import pickle

import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import GradientBoostingRegressor

from keras.activations import relu
from keras.layers import Activation
from keras.models import Sequential
from keras.layers import Dense, Flatten, Conv2D, MaxPooling2D, Reshape, MaxPooling3D
from keras.utils import np_utils
from keras import regularizers
import keras
import code
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from skopt import gp_minimize
from skopt.space import Real, Integer
from skopt.utils import use_named_args
from matplotlib import pyplot as plt

class PlotLosses(keras.callbacks.Callback):
    def on_train_begin(self, logs={}):
        self.i = 0
        self.x = []
        self.losses = []
        self.val_losses = []

        self.fig = plt.figure()

        self.logs = []

    def on_epoch_end(self, epoch, logs={}):
        self.logs.append(logs)
        self.x.append(self.i)
        self.losses.append(logs.get('loss'))
        self.val_losses.append(logs.get('val_loss'))
        self.i += 1
        plt.semilogy(self.x, self.losses) #, label="loss")
        plt.savefig('/home/tubuntu/algoTrading/loss.png')

class Estimator(object):

    def __init__(self, input_size=None):
        self.library = 'keras'
        self.weights_file = '/home/tubuntu/keras.h5'
        self.model = self.create_network()

    def predict(self, x):
        return self.model.predict(x)

    def set_params(self, **params):
        return self.estimator.set_params(**params)

    def create_network(self, kernel_len=961, num_layers=3, hidden_size=2):
        initializer = keras.initializers.glorot_normal()
        model = Sequential()
        model.add(Dense(kernel_len, input_shape=(kernel_len, ), activation='tanh', kernel_initializer=initializer))
        for i in range(num_layers):
            model.add(Dense(hidden_size*kernel_len, activation='tanh', kernel_initializer=initializer))
        model.add(Dense(kernel_len, activation='linear', kernel_initializer=initializer))
        model.compile(loss='mean_squared_error', optimizer='adam', metrics=['mean_absolute_error', 'mean_squared_error'])
        print(model.summary())
        try:
            model.load_weights(self.weights_file)
        except:
            print('could not load weights')
        return model

    def improve_estimator(self, generator, verbose=1):
        checkpoint = keras.callbacks.ModelCheckpoint(self.weights_file, monitor='mean_squared_error', verbose=1, save_best_only=False, mode='min')
        plot_losses = PlotLosses()
        self.model.fit_generator(generator, steps_per_epoch=32, epochs=80, callbacks=[plot_losses, checkpoint])
        self.save_estimator(self.weights_file)

    def save_estimator(self, estim_path):
        self.model.save_weights(self.weights_file)
