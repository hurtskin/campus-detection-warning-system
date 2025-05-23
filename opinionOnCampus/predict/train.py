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
train_dataset = TextCls(voc_dict_path, data_path, data_stop_path, train=True)
cfg.pad_size = train_dataset.max_len_seq

train_data_loader = data_loader(train_dataset, cfg)

# Define Model
lstm_sentiment_cls = Model(cfg)
lstm_sentiment_cls.to(cfg.devices)  # 'cuda' or 'cpu'

# Define Loss
loss_func = nn.CrossEntropyLoss()
optimizer = optim.Adam(lstm_sentiment_cls.parameters(), lr=cfg.lr)
# samples:20000, batch:79, batch_size:256
for epoch in range(cfg.num_epochs):
    for i, batch in enumerate(train_data_loader):
        label, data = batch
        data = torch.tensor(data).to(cfg.devices)
        label = torch.tensor(label, dtype=torch.int64).to(cfg.devices)

        optimizer.zero_grad()
        pred = lstm_sentiment_cls(data)
        loss_val = loss_func(pred, label)
        # epoch是迭代的周期，ite是迭代的批次，val是loss
        print("epoch is {}, ite is {}, val is {}".format(epoch, i, loss_val))
        loss_val.backward()
        optimizer.step()

    # save model
    if epoch % 10 == 0:
        # 模型的所有参数都装在 state_dict 中, 包括 parameters and buffers
        torch.save(lstm_sentiment_cls.state_dict(),"models/{}.pth".format(epoch))