import statistics
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


# hhttps://www.kaggle.com/datasets/yasserh/twitter-tweets-sentiment-dataset
# Positive, Negative and Neutral.


def preprocess_text(text):
    tokens = tokenizer(text)
    tokens = [token for token in tokens if token not in string.punctuation]
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    stemmer = PorterStemmer()
    tokens = [stemmer.stem(token) for token in tokens]
    return tokens


df = pd.read_csv('Tweets.csv')
df['text'] = df['text'].apply(lambda x: " ".join(x.lower() for x in x.split()))

# # df = df.dropna().reset_index(drop=True)
# # print this lines where is nan value
# print(df[df.isna().any(axis=1)])
# print(df.isna().sum())


x = df['text']
y = df['sentiment']
x_train, x_test, y_train, y_test = train_test_split(x, y, stratify=y)

# pd.set_option('display.max_rows', None)


y_train = y_train.map({'positive': 0, 'negative': 1, 'neutral': 2})
y_test = y_test.map({'positive': 0, 'negative': 1, 'neutral': 2})

# y_train = y_train.astype(int)
# y_test = y_test.astype(int)

tokenizer = get_tokenizer("basic_english")

x_train_preprocessed = [preprocess_text(text) for text in x_train]
x_test_preprocessed = [preprocess_text(text) for text in x_test]

# vocab = Counter([token for tokens in x_train_preprocessed for token in tokens])
# vocab_size = len(vocab)



N = 10000
vocab = Counter([token for tokens in x_train_preprocessed for token in tokens])
vocab = Counter(dict(vocab.most_common(N)))
vocab_size = len(vocab) + 1

# Build the word_to_idx dictionary
word_to_idx = {word: idx for idx, (word, _) in enumerate(vocab.items(), 1)}
word_to_idx["<UNK>"] = 0  # Add the <UNK> token

x_train_indices = [[word_to_idx.get(token, 0) for token in tokens] for tokens in x_train_preprocessed]
x_test_indices = [[word_to_idx.get(token, 0) for token in tokens] for tokens in x_test_preprocessed]



# word_to_idx = {word: idx for idx, (word, _) in enumerate(vocab.most_common(), 1)}

# x_train_indices = [[word_to_idx[token] for token in tokens] for tokens in x_train_preprocessed]
# x_test_indices = [[word_to_idx.get(token, 0) for token in tokens] for tokens in x_test_preprocessed]

# seq_len = [len(i) for i in x_train_indices]
#
# max_length = max(seq_len)
# mean_length = statistics.mean(seq_len)
# median_length = statistics.median(seq_len)
#
# print(f"Max length: {max_length}")
# print(f"Mean length: {mean_length}")
# print(f"Median length: {median_length}")

max_seq_length = 10
x_train_padded = [
    seq[:max_seq_length] + [0] * (max_seq_length - len(seq)) if len(seq) < max_seq_length else seq[:max_seq_length] for
    seq in x_train_indices]
x_test_padded = [
    seq[:max_seq_length] + [0] * (max_seq_length - len(seq)) if len(seq) < max_seq_length else seq[:max_seq_length] for
    seq in x_test_indices]

x_train_tensor = torch.tensor(x_train_padded)
x_test_tensor = torch.tensor(x_test_padded)
y_train_tensor = torch.tensor(y_train.values)
y_test_tensor = torch.tensor(y_test.values)

train_dataset = TensorDataset(x_train_tensor, y_train_tensor)
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
test_dataset = TensorDataset(x_test_tensor, y_test_tensor)
test_loader = DataLoader(test_dataset, batch_size=32)


class SentimentRNN(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(SentimentRNN, self).__init__()
        self.embedding = nn.Embedding(input_size, hidden_size)
        self.rnn = nn.RNN(hidden_size, hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        embedded = self.embedding(x)
        output, _ = self.rnn(embedded)
        output = self.fc(output[:, -1, :])
        return output


# Define model parameters
input_size = vocab_size + 1  # Add 1 for padding token
hidden_size = 128
output_size = 3  # as there are 6 classes

model = SentimentRNN(input_size, hidden_size, output_size)

criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

num_epochs = 15
for epoch in range(num_epochs):
    model.train()
    running_loss = 0.0
    num = 0
    for inputs, labels in train_loader:
        num += 1
        # print(f'Batch {num}/{len(train_loader)}')
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        running_loss += loss.item()
    print(f'Epoch {epoch + 1}/{num_epochs}, Loss: {running_loss / len(train_loader)}')

model.eval()
correct = 0
total = 0
with torch.no_grad():
    for inputs, labels in test_loader:
        outputs = model(inputs)
        _, predicted = torch.max(outputs, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

print(f'Accuracy: {correct / total}')
