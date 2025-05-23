import torch
import torch.nn as nn
from torch import optim
from networksmodel import Model
from encapsulate_datasets import data_loader, TextCls
from config import Config

# Define Config object
cfg = Config()

# Load Data
voc_dict_path = "./data/dict.txt"
data_path = "./data/weibo_senti_100k.csv"
data_stop_path = "./data/stopwords.txt"
test_dataset = TextCls(voc_dict_path, data_path, data_stop_path, train=False)
cfg.pad_size = test_dataset.max_len_seq

test_data_loader = data_loader(test_dataset, cfg)

# Define Model
lstm_sentiment_cls = Model(cfg)
lstm_sentiment_cls.to(cfg.devices)  # 'cuda' or 'cpu'

# Load Model        
lstm_sentiment_cls.load_state_dict(torch.load('models/90.pth'))
correct = 0
for i, batch in enumerate(test_data_loader):
    labels, data = batch
    data = torch.tensor(data).to(cfg.devices)
    labels = torch.tensor(labels, dtype=torch.int64).to(cfg.devices)
    out = lstm_sentiment_cls(data)

    predict_loc = torch.argmax(out, dim=1)
    correct += (predict_loc == labels).sum()

print("Test accuracy:{}".format(correct.item()/len(test_dataset)))



