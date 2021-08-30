
## 1. Background
The purpose of this project is to build a text classification model that’s capable of detecting different types of of toxicity like threats, obscenity, insults, and identity-based hate, which is the same as [Kaggle's Toxic Comment Classification Challenge](https://www.kaggle.com/c/jigsaw-toxic-comment-classification-challenge/overview). 


## 2. Dataset
The dataset is originally from comments from Wikipedia’s talk page edits. It can be downloaded from the link: https://www.kaggle.com/c/jigsaw-toxic-comment-classification-challenge/data. Three files from the zipped file will be used, train.csv.zip, test.csv.zip and test_labels.csv.zip. The file train.csv.zip is the training set, contains comments with their binary labels. The file test.csv.zip is the test set which is used to predict the toxicity probabilities for these comments. The test set contains some comments which are not included in scoring. The file test_labels.csv includes labels for the test data; value of -1 indicates it was not used for scoring. Based on the above description, we know that train.csv.zip is used to build the model. The file test.csv.zip and test_labels.csv.zip are used for model testing.

## 3. Model training
The source code is from one of the latest submission which obtained great scores: https://www.kaggle.com/cheeponglee/toxic-comment-multilabel-v2. The author of the code is Chee Pong Lee. The model is trained based on the pre-trained BERT model: 'bert-base-uncased', with 12-layer, 768-hidden, 12-heads and 110M parameters. You can run the notebook with 3 epochs to get model 'toxic_BERT_multilabel'. You can find all training and config details from the source notebook. 


## 4. Model testing
The model testing script is intercepted and modifiled from the last section of the above notebook. The execution of the testing script is as  follows:
```bash
python3 /opt/script/mltc_test.py toxic_BERT_multilabel.pt test.csv.zip test_labels.csv.zip 
```
After running the model testing script, one output file with the name 'text_classification_result.csv' will be generated. The testing result and the testing probabilities will output to this file.
