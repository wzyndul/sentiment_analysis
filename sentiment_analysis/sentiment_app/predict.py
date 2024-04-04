import json
import string

import torch
from nltk import PorterStemmer
from nltk.corpus import stopwords
from torchtext.data import get_tokenizer

from sentiment_app.sentiment_rnn import SentimentRNN

MAX_SEQ_LENGTH = 10
MODEL_PATH = 'sentiment_app/data/sentiment_model.pth'
VOCAB_PATH = 'sentiment_app/data/vocab.json'

model_info = torch.load(MODEL_PATH)
input_size = model_info['input_size']
hidden_size = model_info['hidden_size']
output_size = model_info['output_size']
model = SentimentRNN(input_size, hidden_size, output_size)
model.load_state_dict(model_info['state_dict'])
with open(VOCAB_PATH, 'r') as f:
    word_to_idx = json.load(f)


def preprocess_text(text):
    tokenizer = get_tokenizer("basic_english")
    tokens = tokenizer(text)
    tokens = [token for token in tokens if token not in string.punctuation]
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    stemmer = PorterStemmer()
    tokens = [stemmer.stem(token) for token in tokens]
    return tokens


def predict_sentiment(text):
    model.eval()
    with torch.no_grad():
        preprocessed_text = preprocess_text(text)
        indexed = [word_to_idx.get(token, 0) for token in preprocessed_text]
        if len(indexed) > MAX_SEQ_LENGTH:
            indexed = indexed[:MAX_SEQ_LENGTH]
        elif len(indexed) < MAX_SEQ_LENGTH:
            indexed += [0] * (MAX_SEQ_LENGTH - len(indexed))
        tensor = torch.LongTensor(indexed).unsqueeze(0)
        prediction = model(tensor)
        _, predicted = torch.max(prediction, 1)
        return 1 if predicted.item() == 1 else 0
