This is the demo scripts for running the benchmarking test or run with real project data.

Folders:

./hparams folder contains the yaml file to configure the embedding vector calculation and pre-trained model location

./embeddings folder contains the x-vectors of training data of gender classifier model and x-vectors of testing data, the .csv files specifying training data and testing data are also included in this folder.

./model folder contains the previously trained gender classifier model

./utils folder contains the scripts of computing embedding, train classifier, run gender classification test

Scripts:


./utils/gedetec_s4_compute_embedding.py is to compute the embedding vectors for data specified in .csv file in ./embeddings folder, the configure file should be the .yaml file in ./hparams folder

./utils/gedetec_s5_train_mlp_gender_2.py is to train the gender classifier using the x-vectors of training data, which is stored in ./embeddings  folder. 

./utils/gedetec_s6_test_mlp_gender_2.py is to utlize the gender classifier model contained in ./model folder to run the test on the x-vectors of testing data, which is stored in ./embeddings folder

./run_test.sh is runing the benchmark test on a specific public dataset using the model included in this folder, and generate the performance evaluation in corresponding metric.


To run the benchmarking test, simply run the ./run_test.sh in command line.  
