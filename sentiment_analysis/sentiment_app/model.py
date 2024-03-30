import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F
import nltk
from matplotlib import pyplot as plt
from nltk.corpus import stopwords
from torchtext.data import get_tokenizer
from collections import Counter
import string
import re
from tqdm import tqdm
from torch.utils.data import TensorDataset, DataLoader
from sklearn.model_selection import train_test_split

# https://www.kaggle.com/datasets/nelgiriyewithana/emotions
# sadness (0), joy (1), love (2), anger (3), fear (4), and surprise (5)


def preprocess_text(text):
    tokens = tokenizer(text)
    tokens = [token for token in tokens if token not in string.punctuation]
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    return tokens




df = pd.read_csv('data.csv')
df = df.dropna()
x = df['text']
y = df['label']
x_train, x_test, y_train, y_test = train_test_split(x, y, stratify=y)

y_train = y_train.values
y_test = y_test.values


tokenizer = get_tokenizer("basic_english")

x_train_preprocessed = [preprocess_text(text) for text in x_train]
x_test_preprocessed = [preprocess_text(text) for text in x_test]



vocab = Counter([token for tokens in x_train_preprocessed for token in tokens])
vocab_size = len(vocab)
word_to_idx = {word: idx for idx, (word, _) in enumerate(vocab.most_common(), 1)}

x_train_indices = [[word_to_idx[token] for token in tokens] for tokens in x_train_preprocessed]
x_test_indices = [[word_to_idx.get(token, 0) for token in tokens] for tokens in x_test_preprocessed]

train_sequence_lengths = [len(seq) for seq in x_train_indices]
test_sequence_lengths = [len(seq) for seq in x_test_indices]

max_seq_length = 50
x_train_padded = [seq[:max_seq_length] + [0] * (max_seq_length - len(seq)) if len(seq) < max_seq_length else seq[:max_seq_length] for seq in x_train_indices]
x_test_padded = [seq[:max_seq_length] + [0] * (max_seq_length - len(seq)) if len(seq) < max_seq_length else seq[:max_seq_length] for seq in x_test_indices]


x_train_tensor = torch.tensor(x_train_padded)
y_train_tensor = torch.tensor(y_train)
x_test_tensor = torch.tensor(x_test_padded)
y_test_tensor = torch.tensor(y_test)

train_dataset = TensorDataset(x_train_tensor, y_train_tensor)
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
test_dataset = TensorDataset(x_test_tensor, y_test_tensor)
test_loader = DataLoader(test_dataset, batch_size=32)
