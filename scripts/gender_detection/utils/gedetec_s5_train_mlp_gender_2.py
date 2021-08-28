'''

20210714:
    This script it to train a Multip-Layer Perceptron (MLP) classifier from a input training vector.

    Input: x-vector
------------------------------------------------------------

'''

import os
import sys
import speechbrain as sb
import pickle
from hyperpyyaml import load_hyperpyyaml
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.datasets import make_classification


if __name__ == "__main__":
    if (len(sys.argv) != 2):
        print("\n    Usage: " + sys.argv[0] + " x_vector_file (a **_stat_obj.pkl file including x-vector)")
        print("           x-vector eg1. voxCeleb1_train_embeddings_stat_obj.pkl")
        print("           x-vector eg2. voxCeleb1_train_embeddings_stat_obj_126vs126.pkl")
        print("\n")
        sys.exit(0)

    script_name = sys.argv[0]
    x_vector_file = sys.argv[1]

    print("\n")
    print("    script_name = ", script_name)
    print("    x_vector_file = ", x_vector_file)
    print("\n")

    fin = open(x_vector_file, "rb")
    embeddings_stat_obj = pickle.load(fin)
    print("  type(embeddings_stat_obj) = ", type(embeddings_stat_obj))
    print("  embeddings_stat_obj = \n", embeddings_stat_obj)

    x_train = embeddings_stat_obj.stat1
    y_train = embeddings_stat_obj.modelset
    y_train = np.where( y_train == 'm', 0, y_train)  
    y_train = np.where( y_train == 'f', 1, y_train) 
    y_train = y_train.astype(int)
    print("  x_train = \n", x_train)
    print("  y_train = \n", y_train)
    print("  x_train.shape = ", x_train.shape)
    print("  y_train.shape = ", y_train.shape)
    print("  type(x_train) = ", type(x_train))
    print("  type(y_train) = ", type(y_train))

    
    #clf = MLPClassifier(hidden_layer_sizes=500, random_state=1, max_iter=100)
    clf = MLPClassifier(hidden_layer_sizes=500, random_state=1, max_iter=200, verbose=True)
    #clf = MLPClassifier(hidden_layer_sizes=500, random_state=1, max_iter=300)
    #clf = MLPClassifier(hidden_layer_sizes=(500,500), random_state=1, max_iter=100)
    #clf = MLPClassifier(hidden_layer_sizes=(500,500), random_state=1, max_iter=200)
    #clf = MLPClassifier(hidden_layer_sizes=(500,500), random_state=1, max_iter=300)
    #clf = MLPClassifier(hidden_layer_sizes=1000, random_state=1, max_iter=100)
    #clf = MLPClassifier(hidden_layer_sizes=1000, random_state=1, max_iter=200)
    #clf = MLPClassifier(hidden_layer_sizes=1000, random_state=1, max_iter=300)


    #clf = MLPClassifier(hidden_layer_sizes=10, random_state=1, max_iter=100)
    #clf = MLPClassifier(hidden_layer_sizes=50, random_state=1, max_iter=300)
    #clf = MLPClassifier(hidden_layer_sizes=58, random_state=1, max_iter=300)
    #clf = MLPClassifier(hidden_layer_sizes=65, random_state=1, max_iter=300)
    #clf = MLPClassifier(hidden_layer_sizes=75, random_state=1, max_iter=300)
    #clf = MLPClassifier(hidden_layer_sizes=100, random_state=1, max_iter=300)
    #clf = MLPClassifier(hidden_layer_sizes=500, random_state=1, max_iter=300)
    #clf = MLPClassifier(hidden_layer_sizes=1000, random_state=1, max_iter=200)
    #clf = MLPClassifier(hidden_layer_sizes=2000, random_state=1, max_iter=500, verbose=True)
    #clf = MLPClassifier(hidden_layer_sizes=(2000,2000), random_state=1, max_iter=100)
    #clf = MLPClassifier(hidden_layer_sizes=4000, random_state=1, max_iter=100) 
    #clf = MLPClassifier(hidden_layer_sizes=(100, 100),random_state=1, max_iter=10)
    #clf = MLPClassifier(hidden_layer_sizes=(100, 100),random_state=1, max_iter=100)
    #clf = MLPClassifier(hidden_layer_sizes=(100, 100),random_state=1, max_iter=300)
    #clf = MLPClassifier(hidden_layer_sizes=(100, 100),random_state=1, max_iter=600)
    #clf = MLPClassifier(hidden_layer_sizes=(100, 100),random_state=1, max_iter=1000)

    print("  clf = ", clf)
    clf.fit(x_train, y_train)
    print("  MLP training completed")

    y_train_predict = clf.predict(x_train)
    print("  y_train_predict = \n", y_train_predict)
    print("  y_train_predict.shape = ", y_train_predict.shape)

    score = clf.score(x_train, y_train)
    print("  score = ", score)

    model_name = "classifier_gender.pkl"
    fout = open(model_name, "wb")
    pickle.dump(clf, fout)
    print("  $$$ output model file: classifer_gender.pkl")
