import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from config import Config


class Model(nn.Module):
    def __init__(self, config):
        super(Model, self).__init__()
        # padding_idx – If specified, the entries at :attr:`padding_idx` do not contribute
        # to the gradient; therefore, the embedding vector at :attr:`padding_idx` is not
        # updated during training, i.e. it remains as a fixed "pad".
        self.embedding = nn.Embedding(config.n_vocab, config.embedding_size,
                                      padding_idx=config.n_vocab - 1)  # The last index in vocabulary do not
        # participate in gradient update, data size=(batch_size, sequence_size, embed_size)
        # Define RNN Neural Networks
        self.lstm = nn.LSTM(config.embedding_size,
                            config.hidden_size,
                            config.num_layers,
                            batch_first=True,
                            dropout=config.dropout)  # dropout prevent over-fitting
        # Define Convolutional Neural Networks
        # 采用一维MaxPooling,因为LSTM的输出是hn dimension:(num_layers, batch_size, hidden_size)，hidden_size是一维的。
        # kernel_size (Union[int, Tuple[int]]) – The size of the sliding window, must be > 0.
        # stride (Union[int, Tuple[int]]) – The stride of the sliding window, must be > 0.
        # Default value for padding is 0
        # L_out = floor((n - m + 2p) / s) + 1
        self.maxpool = nn.MaxPool1d(kernel_size=config.pad_size)
        # Define full connection layer
        self.fc = nn.Linear(config.hidden_size + config.embedding_size,
                            config.num_classes)
        self.softmax = nn.Softmax(dim=1)

    def forward(self, x):
        embed = self.embedding(x)
        # Return output, (hn, cn), output_size:(batch_size, sequence_length, hidden_size);
        # hn_size:(num_layers, batch_size, hidden_size);
        # cn_size:(num_layers, batch_size, hidden_size)
        out, _ = self.lstm(embed)  # (h0, c0) are not provided, so the initial values are 0 vector.
        out = torch.cat((embed, out), dim=2)  # 在第2个维度进行拼接
        out = F.relu(out)  # out的负数值被赋予0
        out = out.permute(0, 2, 1)  # [1,8,256]->[1,256,8],sequence_size:8, embed_size:256
        # 根据公式：L_out = floor((n - m + 2p) / s) + 1，L_out==1，maxpool从最后8个数值中选一个最大的，sequence中所有词都读出来了
        out = self.maxpool(out).reshape(out.size()[0], -1)  # 转换成2维度的tensor
        out = self.fc(out)  # fc as a classification layer:(1,256)->(1.2)
        out = self.softmax(out)
        return out


if __name__ == '__main__':
    cfg = Config()
    cfg.pad_size = 8
    sentiment_cls = Model(config=cfg)
    # batch_size:1, sequence_length:640
    input_tensor = torch.tensor([i for i in range(8)]).reshape(1, 8)
    out_tensor = sentiment_cls(input_tensor)
    print("out_tensor.size:{0}, out_tensor:{1}".format(out_tensor.size(), out_tensor))
