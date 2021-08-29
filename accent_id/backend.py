#!/usr/bin/env python3
import numpy as np
from sklearn import preprocessing
from sklearn.naive_bayes import GaussianNB
import pickle

xvector_file_train = 'exp/xvectors_train_20000/vector_norm.txt'
label_file_train = 'data/train_20000/utt2spk'
xvector_file_test = 'exp/xvectors_test_20000/vector_norm.txt'
label_file_test = 'data/test_20000/utt2lang'

xvectors_train = []
xvectors_test = []
labels = []

fl = open(label_file_train, 'r')
for line in fl:
    labels.append(line.strip().split()[-1])
fl = open(label_file_test, 'r')
for line in fl:
    labels.append(line.strip().split()[-1])

le = preprocessing.LabelEncoder()
labels_encoded = le.fit_transform(labels)

fx_train = open(xvector_file_train, 'r')
for line in fx_train:
    xvector = line.strip().split()[2:-1]
    xvector_float = [float(item) for item in xvector]
    xvectors_train.append(tuple(xvector_float))
num_train = len(xvectors_train)
labels_encoded_train = labels_encoded[0:num_train]

fx = open(xvector_file_test, 'r')
for line in fx:
    xvector = line.strip().split()[2:-1]
    xvector_float = [float(item) for item in xvector]
    xvectors_test.append(tuple(xvector_float))
num_test = len(xvectors_test)
labels_encoded_test = labels_encoded[-num_test:]




model = GaussianNB()
model.fit(xvectors_train, labels_encoded_train)
filename = 'guassian_model.sav'
pickle.dump(model, open(filename, 'wb'))
#model = pickle.load(open(filename, 'rb'))
results = model.predict(xvectors_test)
#xvector_np = np.array(xvectors)







