import numpy as np
import pandas as pd
import torch.nn as nn
import torch.nn.functional as F
import nltk
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
    tokens = tokenizer(text.lower())
    tokens = [token for token in tokens if token not in string.punctuation]
    tokens = [token for token in tokens if token not in stopwords.words('english')]
    return tokens



df = pd.read_csv('data.csv')
df = df.dropna()
x = df['text']
y = df['label']
x_train, x_test, y_train, y_test = train_test_split(x, y, stratify=y)

tokenizer = get_tokenizer("basic_english")

x_train_preprocessed = [preprocess_text(text) for text in x_train[:5]]
x_test_preprocessed = [preprocess_text(text) for text in x_test[:5]]

