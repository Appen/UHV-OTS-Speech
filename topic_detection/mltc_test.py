
import time
import datetime
import sys
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import hamming_loss, accuracy_score

# import pyTorch
import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim import lr_scheduler


# import pyTorch
import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim import lr_scheduler
# import other parts of transformers as well as tqdm
from transformers import (AutoTokenizer, AutoModel,
                                  AutoModelForSequenceClassification,
                                                            DataCollatorWithPadding, AdamW, get_scheduler,
                                                                                      get_linear_schedule_with_warmup,)
# import pyarrow (can only import this with GPU on kaggle notebook)
import pyarrow as pa
from tqdm.auto import tqdm
from torch.utils.data import TensorDataset, DataLoader, RandomSampler, SequentialSampler
import datasets
import random
from sklearn.metrics import classification_report


def format_time(elapsed):
    '''
    Takes a time in seconds and returns a string hh:mm:ss
    '''
    # Round to the nearest second.
    elapsed_rounded = int(round((elapsed)))
    
    # Format as hh:mm:ss
    return str(datetime.timedelta(seconds=elapsed_rounded))


if __name__=='__main__':
    if (len(sys.argv) != 4):
        print("\n")
        print("    Usage: " + sys.argv[0] + "  model  test.csv  test_labels.csv")
        print("\n")
        sys.exit(0)

    model_file = sys.argv[1]
    test_file = sys.argv[2]
    test_label_file = sys.argv[3]

    print("\n")
    print("  model_file = ", model_file)
    print("  test_file = ", test_file)
    print("  test_label_file = ", test_label_file)
    print("\n")

    checkpoint = "bert-base-uncased"
    tokenizer = AutoTokenizer.from_pretrained(checkpoint)
    model = AutoModelForSequenceClassification.from_pretrained(checkpoint, num_labels = 6)
    state_dict = torch.load(model_file, map_location='cpu')
    model.load_state_dict(state_dict)
    model.eval()
    
    device = torch.device("cuda:0") if torch.cuda.is_available() else torch.device("cpu")
    print("  device = ", device)
    model.to(device)

    test_csv = pd.read_csv(test_file)
    test_csv_labels = pd.read_csv(test_label_file)

    #test_csv = test_csv.head(100)
    print("  test_csv = \n", test_csv)
    print("  len(test_csv) = ", len(test_csv))

    # tokenize and encode sequences in the actual test set
    sub_tokens = tokenizer.batch_encode_plus(test_csv["comment_text"].tolist(),
                                         max_length = 200,
                                         pad_to_max_length=True,
                                         truncation=True,
                                         return_token_type_ids=False)

    sub_seq = torch.tensor(sub_tokens['input_ids'])
    sub_mask = torch.tensor(sub_tokens['attention_mask'])

    sub_data = TensorDataset(sub_seq, sub_mask)
    # dataLoader for validation set
    batch_size = 256
    sub_dataloader = DataLoader(sub_data, batch_size=batch_size)

    # Measure how long the evaluation going to takes.
    t0 = time.time()

    for step, batch in enumerate(sub_dataloader):
        # Progress update every 40 batches.
        if step % 40 == 0 and not step == 0:
            # Calculate elapsed time in minutes.
            elapsed = format_time(time.time() - t0)
            # Report progress.
            print('  Batch {:>5,}  of  {:>5,}.    Elapsed: {:}.'.format(step, len(sub_dataloader), elapsed))
        b_input_ids = batch[0].to(device)
        b_input_mask = batch[1].to(device)
        with torch.no_grad():
            outputs = model(b_input_ids, b_input_mask)
            pred_probs = torch.sigmoid(outputs.logits)
            if step == 0: predictions = pred_probs.cpu().detach().numpy()
            else: predictions = np.append(predictions, pred_probs.cpu().detach().numpy(), axis=0)
    
    categories = ['toxic','severe_toxic','obscene','threat','insult','identity_hate']
    predictions_df = pd.DataFrame(predictions, columns = categories)
    print("  predictions_df.shape = ", predictions_df.shape)
    print("  len(predictions_df) = ", len(predictions_df))


    submission = pd.concat([test_csv["id"], predictions_df], axis=1)
    print("  submission.shape = ", submission.shape)
    print("  submission = \n", submission)

    submission.to_csv('text_classification_result.csv', index=False, header=True)
