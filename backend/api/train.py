import json
import pandas as pd
import torch
import torch.nn as nn

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from torchtext.data import get_tokenizer
from collections import Counter
import string
from torch.utils.data import TensorDataset, DataLoader
from sklearn.model_selection import train_test_split

from api.sentiment_rnn import SentimentRNN


# hhttps://www.kaggle.com/datasets/yasserh/twitter-tweets-sentiment-dataset
# Positive, Negative and Neutral.

class SentimentAnalysis:
    def __init__(self):
        self.tokenizer = get_tokenizer("basic_english")
        self.input_size = None
        self.hidden_size = 64
        self.output_size = 2
        self.model = None
        self.train_loader = None
        self.test_loader = None
        self.word_to_idx = None
        self.max_seq_length = None

    def preprocess_text(self, text):
        tokens = self.tokenizer(text)
        tokens = [token for token in tokens if token not in string.punctuation]
        stop_words = set(stopwords.words('english'))
        tokens = [token for token in tokens if token not in stop_words]
        stemmer = PorterStemmer()
        tokens = [stemmer.stem(token) for token in tokens]
        return tokens

    def load_data(self):
        # df = pd.read_csv('200k.csv', encoding='ISO-8859-1')
        df = pd.read_csv('data/Tweets.csv')
        df['text'] = df['text'].apply(lambda x: " ".join(x.lower() for x in x.split()))
        x = df['text']
        y = df['sentiment']
        # y = df['target']
        x_train, x_test, y_train, y_test = train_test_split(x, y, stratify=y)
        y_train = y_train.map({'positive': 0, 'negative': 1, 'neutral': 2})
        y_test = y_test.map({'positive': 0, 'negative': 1, 'neutral': 2})
        x_train = x_train[y_train != 2]
        y_train = y_train[y_train != 2]
        x_test = x_test[y_test != 2]
        y_test = y_test[y_test != 2]

        x_train_preprocessed = [self.preprocess_text(text) for text in x_train]
        x_test_preprocessed = [self.preprocess_text(text) for text in x_test]
        vocab = Counter([token for tokens in x_train_preprocessed for token in tokens])
        self.input_size = len(vocab) + 2  # Add 1 for padding token and 1 for <UNK> token
        self.word_to_idx = {word: idx for idx, (word, _) in enumerate(vocab.items(), 1)}
        self.word_to_idx["<UNK>"] = 0  # Add the <UNK> token

        self.max_seq_length = 10
        x_train_indices = [[self.word_to_idx.get(token, 0) for token in tokens] for tokens in x_train_preprocessed]
        x_test_indices = [[self.word_to_idx.get(token, 0) for token in tokens] for tokens in x_test_preprocessed]
        x_train_padded = [seq[:self.max_seq_length] + [0] * (self.max_seq_length - len(seq)) if len(
            seq) < self.max_seq_length else seq[:self.max_seq_length] for seq in x_train_indices]
        x_test_padded = [seq[:self.max_seq_length] + [0] * (self.max_seq_length - len(seq)) if len(
            seq) < self.max_seq_length else seq[:self.max_seq_length] for seq in x_test_indices]

        # seq_len = [len(i) for i in x_train_indices]

        # max_length = max(seq_len)
        # mean_length = statistics.mean(seq_len)
        # median_length = statistics.median(seq_len)

        # print(f"Max length: {max_length}")
        # print(f"Mean length: {mean_length}")
        # print(f"Median length: {median_length}")

        x_train_tensor = torch.tensor(x_train_padded)
        x_test_tensor = torch.tensor(x_test_padded)
        y_train_tensor = torch.tensor(y_train.values)
        y_test_tensor = torch.tensor(y_test.values)
        train_dataset = TensorDataset(x_train_tensor, y_train_tensor)
        self.train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
        test_dataset = TensorDataset(x_test_tensor, y_test_tensor)
        self.test_loader = DataLoader(test_dataset, batch_size=32, shuffle=True)

    def train_model(self):
        self.model = SentimentRNN(self.input_size, self.hidden_size, self.output_size)
        criterion = nn.CrossEntropyLoss()
        optimizer = torch.optim.Adam(self.model.parameters(), lr=0.001, weight_decay=1e-5)
        num_epochs = 10
        for epoch in range(num_epochs):
            self.model.train()
            running_loss = 0.0
            correct_predictions = 0
            total_predictions = 0
            for inputs, labels in self.train_loader:
                optimizer.zero_grad()
                outputs = self.model(inputs)
                _, predicted = torch.max(outputs, 1)
                loss = criterion(outputs, labels)
                loss.backward()
                optimizer.step()
                running_loss += loss.item()
                correct_predictions += (predicted == labels).sum().item()
                total_predictions += labels.size(0)
            print(f'Epoch {epoch + 1}/{num_epochs}, Loss: {running_loss / len(self.train_loader)}')

    def test_model(self):
        self.model.eval()
        correct = 0
        total = 0
        with torch.no_grad():
            for inputs, labels in self.test_loader:
                outputs = self.model(inputs)
                _, predicted = torch.max(outputs, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()
        print(f'Accuracy: {correct / total}')

    def save_model(self, model_path, vocab_path):
        model_info = {
            'state_dict': self.model.state_dict(),
            'input_size': self.input_size,
            'hidden_size': self.hidden_size,
            'output_size': self.output_size
        }
        torch.save(model_info, model_path)
        with open(vocab_path, 'w') as f:
            json.dump(self.word_to_idx, f)


sa = SentimentAnalysis()
sa.load_data()
sa.train_model()
sa.test_model()
# sa.save_model('sentiment_model.pth', 'vocab.json')
