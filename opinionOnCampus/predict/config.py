import torch.types


class Config:
    def __init__(self):
        self.n_vocab = 3002  # 字典长度
        self.embedding_size = 128
        self.hidden_size = 128
        self.num_layers = 3  # The layers of lstm
        self.dropout = 0.8
        self.num_classes = 2
        self.pad_size = 32  # The max length of sequence
        self.devices = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.batch_size = 256
        self.is_shuffle = True
        self.lr = 0.001
        self.num_epochs = 1


