#!/usr/bin/python3
'''
20210712:
    This script is to do MLP model testing for gender detection.
------------------------------------------------------------------


'''

import os
import sys
import pickle
import torch
import speechbrain as sb
import numpy
from hyperpyyaml import load_hyperpyyaml
import speechbrain as sb
from speechbrain.processing.PLDA_LDA import StatObject_SB


from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


def gender_model_testing(test_stat_obj):
    x_test = test_stat_obj.stat1
    print("  x_test = \n", x_test)
    print("  x_test.shape = ", x_test.shape)

    x_test_id = test_stat_obj.segset
    print("  x_test_id = \n", x_test_id)
    print("  x_test_id.shape = ", x_test_id.shape)
    
    y_test = test_stat_obj.modelset
    print("  y_test = \n", y_test)
    y_test = numpy.where( y_test == 'm', 0, y_test)
    y_test = numpy.where( y_test == 'f', 1, y_test)
    y_test = y_test.astype(int)
    print("  y_test = \n", y_test)
    print("  y_test.shape = ", y_test.shape)
    
    y_predict = clf.predict(x_test)
    print("  y_predict = \n", y_predict)
    print("  y_predict.shape = ", y_predict.shape)

    y_predict_label = numpy.where(  y_predict == 0, 'm', y_predict)
    y_predict_label = numpy.where(  y_predict == 1, 'f', y_predict_label)
    print("  y_predict_label = \n", y_predict_label)
    print("  y_predict_label.shape = ", y_predict_label.shape)

    y_predict_prob = clf.predict_proba(x_test)
    print("  y_predict_prob = \n", y_predict_prob)
    print("  y_predict_prob.shape = ", y_predict_prob)

    y_predict_prob_max = numpy.max(y_predict_prob, axis=1)
    print("  y_predict_prob_max = \n", y_predict_prob_max)
    print("  y_predict_prob_max.shape = ", y_predict_prob_max.shape)

    #max_prob_index_arr = numpy.argmax(y_predict_prob, axis=1)
    #print("  max_prob_index_arr = ", max_prob_index_arr)
    #print("  max_prob_index_arr.shape = ", max_prob_index_arr.shape)
    #print("  max_prob_index_arr.dtype = ", max_prob_index_arr.dtype)

    score = clf.score(x_test, y_test)
    print("  score = ", score)

    accuracy = accuracy_score(y_test, y_predict)
    print("  accuracy = ", accuracy)

  
    fname = "gender_detection_result.txt"
    fout = open(fname, "w")
    fout.write("utterance_id,predict_gender,probability\n")
    for ii in range(len(x_test_id.tolist())):
        fout.write(str(x_test_id[ii]) + "," + y_predict_label[ii] + "," + str(y_predict_prob_max[ii]) + "\n")
    fout.close()
    print("\n  $$$ output file: ", fname, "\n")


if __name__ == "__main__":
    if (len(sys.argv) != 3):
        print("\n")
        print("  Usage: " + sys.argv[0] + " model_file(*.pkl) test_x_vector_file(*_stat_obj.pkl)")
        print("\n")
        sys.exit(0)

    script_name = sys.argv[0]
    model_name = sys.argv[1]
    x_vector_file = sys.argv[2]

    #model_path = os.path.join(params_save_folder, 'clf_mlp.pkl')
    #print("  model_path = ", model_path)
    print("\n")
    print("  script_name = ", script_name)
    print("  model_name = ", model_name)
    print("  x_vector_file = ", x_vector_file)
    print("\n")

    clf = sb.dataio.dataio.load_pickle(model_name)
    print("  clf = ", clf)

    fin = open(x_vector_file, "rb")
    test_stat_obj = pickle.load(fin)

    gender_model_testing(test_stat_obj)
