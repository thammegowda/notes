######################## CSCI567 - HW4 Code ###############################
# Author: Nitin Kamra
# Email: nkamra@usc.edu
###########################################################################

###################### Deep Learning HW utilities #########################

import numpy as np

from keras.layers import Input, Dense
from keras.models import Sequential
import keras.regularizers as Reg
from keras.optimizers import SGD
from keras.callbacks import EarlyStopping
from keras.utils.np_utils import to_categorical
from time import time

def genmodel(num_units, actfn='relu', reg_coeff=0.0, last_act='softmax'):
	''' Generate a neural network model of approporiate architecture
	Args:
		num_units: architecture of network in the format [n1, n2, ... , nL]
		actfn: activation function for hidden layers ('relu'/'sigmoid'/'linear'/'softmax')
		reg_coeff: L2-regularization coefficient
		last_act: activation function for final layer ('relu'/'sigmoid'/'linear'/'softmax')
	Output:
		model: Keras sequential model with appropriate fully-connected architecture
	'''

	model = Sequential()
	for i in range(1, len(num_units)):
		if i == 1 and i < len(num_units) - 1:
			model.add(Dense(input_dim=num_units[0], output_dim=num_units[i], activation=actfn,
				W_regularizer=Reg.l2(l=reg_coeff), init='glorot_normal'))
		elif i == 1 and i == len(num_units) - 1:
			model.add(Dense(input_dim=num_units[0], output_dim=num_units[i], activation=last_act,
				W_regularizer=Reg.l2(l=reg_coeff), init='glorot_normal'))
		elif i < len(num_units) - 1:
			model.add(Dense(output_dim=num_units[i], activation=actfn,
				W_regularizer=Reg.l2(l=reg_coeff), init='glorot_normal'))
		elif i == len(num_units) - 1:
			model.add(Dense(output_dim=num_units[i], activation=last_act,
				W_regularizer=Reg.l2(l=reg_coeff), init='glorot_normal'))
	return model


def loaddata(filename):
	''' Load and preprocess dataset
	Args:
		filename: Full relative path and file name of the dataset: MiniBooNE_PID.txt
	Output:
		X_tr: 50 dimensional training features
		y_tr: 2 dimensional categorical training labels
		X_te: 50 dimensional test features
		y_te: 2 dimensional categorical test labels
	'''
	X = np.loadtxt(filename, skiprows=1)
	with open(filename, 'rb') as f:
		header = f.readline()
	f.close()
	header_list = header.split()
	num_sig = int(header_list[0])
	num_bg = int(header_list[1])
	y = np.append(np.ones(num_sig), np.zeros(num_bg))

	data = np.append(X, np.reshape(y, [y.shape[0], 1]), axis=1)
	n_tr = int(0.8*(num_sig + num_bg))
	n_te = num_sig + num_bg - n_tr
	np.random.shuffle(data)

	X_tr = data[0:n_tr,0:-1]
	y_tr = data[0:n_tr,-1]
	y_tr = to_categorical(y_tr)
	X_te = data[n_tr:,0:-1]
	y_te = data[n_tr:,-1]
	y_te = to_categorical(y_te)
	return X_tr,y_tr,X_te,y_te


def normalize(X_tr, X_te):
	''' Normalize training and test data features
	Args:
		X_tr: Unnormalized training features
		X_te: Unnormalized test features
	Output:
		X_tr: Normalized training features
		X_te: Normalized test features
	'''
	X_mu = np.mean(X_tr, axis=0)
	X_tr = X_tr - X_mu
	X_sig = np.std(X_tr, axis=0)
	X_tr = X_tr/X_sig
	X_te = (X_te - X_mu)/X_sig
	return X_tr, X_te


def testmodels(X_tr, y_tr, X_te, y_te, archs, actfn='relu', last_act='softmax', reg_coeffs=[0.0],
				num_epoch=30, batch_size=1000, sgd_lr=1e-5, sgd_decays=[0.0], sgd_moms=[0.0],
					sgd_Nesterov=False, EStop=False, verbose=0):
	''' Train and test neural network architectures with varying parameters
	Args:
		X_tr: Training features
		y_tr: Training labels
		X_te: Test features
		y_te: Test labels
		archs: List of architectures
		actfn: activation function for hidden layers ('relu'/'sigmoid'/'linear'/'softmax')
		last_act: activation function for final layer ('relu'/'sigmoid'/'linear'/'softmax')
		reg_coeffs: Lsit of L2-regularization coefficients
		num_epoch: number of iterations for SGD
		batch_size: batch size for gradient descent
		sgd_lr: Learning rate for SGD
		sgd_decays: List of decay parameters for the learning rate
		sgd_moms: List of momentum coefficients, works only if sgd_Nesterov = True
		sgd_Nesterov: Boolean variable to use/not use momentum
		EStop: Boolean variable to use/not use early stopping
		verbose: 0 or 1 to determine whether keras gives out training and test progress report
	'''
	[n_tr,d] = X_tr.shape
	[n_te,d] = X_te.shape
	best_acc = 0
	best_config = []
	call_ES = EarlyStopping(monitor='val_acc', patience=6, verbose=1, mode='auto')
	counter = 0
	times = []
	for arch in archs:
		for reg_coeff in reg_coeffs:
			for sgd_decay in sgd_decays:
				for sgd_mom in sgd_moms:
					st = time()
					# Generate Model
					model = genmodel(num_units=arch, actfn=actfn, reg_coeff=reg_coeff,
						last_act=last_act)
					# Compile Model
					sgd = SGD(lr=sgd_lr, decay=sgd_decay, momentum=sgd_mom,
						nesterov=sgd_Nesterov)
					model.compile(loss='categorical_crossentropy', optimizer=sgd,
						metrics=['accuracy'])
					# Train Model
					if EStop:
						model.fit(X_tr, y_tr, nb_epoch=num_epoch, batch_size=batch_size,
							verbose=verbose, callbacks=[call_ES], validation_split=0.1,
							validation_data=None, shuffle=True)
					else:
						model.fit(X_tr, y_tr, nb_epoch=num_epoch, batch_size=batch_size,
							verbose=verbose)
					tt = time() - st # time taken
					times.append(tt)
					# Evaluate Models
					score = model.evaluate(X_te, y_te, batch_size=batch_size, verbose=verbose)
					if score[1] > best_acc:
						best_acc = score[1]
						best_config = [arch, reg_coeff, sgd_decay, sgd_mom, actfn, best_acc]
					print('architecture={0}, lambda={1}, decay={2}, momentum={3}, actfn={4}: score={5} | time={6}'.format(arch, reg_coeff, sgd_decay, sgd_mom, actfn, score[1], tt))
	print('Best Config: architecture = {0}, lambda = {1}, decay = {2}, momentum = {3}, actfn = {4}, best_acc = {5}'.format(best_config[0], best_config[1], best_config[2], best_config[3], best_config[4], best_config[5]))
	times = np.array(times)
	print("Mean Time = {0}seconds, |Models| = {1}, Total Time = {2}seconds".format(times.mean(), len(times), np.sum(times)))
	return best_config, times
