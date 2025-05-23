from torch.utils.data import Dataset, DataLoader
import jieba
import numpy as np
from config import Config


# Read dictionaries
def read_dict(voc_dict_path):
    voc_dict = {}
    dict_list = open(voc_dict_path, encoding='utf8').readlines()
    for item in dict_list:
        item = item.split(',')
        # ID must be int type
        voc_dict[item[0]] = int(item[1].strip())  # key: value
    return voc_dict


# Load data
def load_data(data_path: str, data_stop_path: str, train: bool = True, train_size: float = 0.7):
    """
     Parameters:
       data_path (str): The path of weibo_senti_100k data.
       data_stop_path(int): The path of stopwords.txt.
       train(bool): If train is True, load train datasets, otherwise load test datasets.
       train_size(float): The split proportion between train and test datasets
       Returns:
       tuple: data(list):[label,seg_res], max_len_seq.
     """
    data_list = open(data_path, encoding='utf8').readlines()[1:]
    np.random.shuffle(data_list)  # Shuffle positive samples and negative samples
    data_list = data_list[:30000] # 算力有限只选则前30000条

    stop_words = open(data_stop_path, encoding='utf8').readlines()
    # 过滤停用词换行符
    stop_words = [line.strip() for line in stop_words]
    # Add ' ' and '\n', 停用词里加会被line.strip()过滤掉
    stop_words.append(" ")  # 停用词添加空格
    stop_words.append("\n")  # 停用词添加回车
    voc_dict = {}
    data = []
    max_len_seq = 0  # 最长的句子长度

    train_data = data_list[:int(len(data_list) * train_size)]
    test_data = data_list[int(len(data_list) * train_size):]
    print("Train data size: ", len(train_data))
    print("Test data size: ", len(test_data))
    if train:
        split_list = train_data
    else:
        split_list = test_data

    for item in split_list:  # 控制读取多少行
        # Obtain labels
        label = item[0]
        # The first item is comma
        content = item[2:].strip()  # Strip the leading and heading space
        # jiaba Chinese segmentation
        seg_list = jieba.cut(content, cut_all=False)
        # Filter all stop words of the list
        seg_res = []
        # 对分出的每一行单词列表进行处理
        for seg_item in seg_list:
            # Determine whether seg_item in the stop_words
            if seg_item not in stop_words:
                seg_res.append(seg_item)

        # 如果当前分词列表长度大于最长序列单词长度，则进行替换
        if len(seg_res) > max_len_seq:
            max_len_seq = len(seg_res)
        # Add label and the weibo list obtained through word segmentation
        data.append([label, seg_res])

    return data, max_len_seq


# 封装数据集
# The subClass of Dataset should inherit __len__ and __getitem__ method
class TextCls(Dataset):

    def __init__(self, voc_dict_path, data_path, data_stop_path, train: bool = True):
        self.data_path = data_path
        self.data_stop_path = data_stop_path

        # Load vocabulary dictionary, word-index table
        self.voc_dict = read_dict(voc_dict_path)
        # Load Data
        self.data, self.max_len_seq = \
            load_data(data_path, data_stop_path, train)
        np.random.shuffle(self.data)

    def __len__(self):
        return len(self.data)

    # Retrieve label and word_list given item from data
    def __getitem__(self, item):
        data = self.data[item]
        label = int(data[0])  # label必须是int
        word_list = data[1]
        # Retrieve voc_dict and convert the word to corresponding ID
        input_idx = []
        for word in word_list:
            if word in self.voc_dict.keys():
                input_idx.append(self.voc_dict[word])  # 单词在词典中，添加对应的索引
            else:
                input_idx.append(self.voc_dict['<UNK>'])  # otherwise add unknown index
        # Determine whether input_idx is aligned with max_seq_len. If it is not aligned,
        # padding input_idx to guaranteed to align with max_seq_len
        if len(input_idx) < self.max_len_seq:
            input_idx += [self.voc_dict['<PAD>'] for _ in range(self.max_len_seq - len(input_idx))]

        data = np.array(input_idx)
        return label, data


# 定义自己的数据加载器
def data_loader(dataset, config):
    # Data loader combines a dataset and a sampler, and provides an iterable over the given dataset.
    return DataLoader(dataset, batch_size=config.batch_size, shuffle=config.is_shuffle)  # 每个批次有10个sequence


if __name__ == '__main__':

    cfg = Config()
    voc_dict_path = "./data/dict.txt"
    data_path = "./data/weibo_senti_100k.csv"
    data_stop_path = "./data/stopwords.txt"

    train_dataset = TextCls(voc_dict_path, data_path, data_stop_path, train=True)

    train_data_loader = data_loader(train_dataset, cfg)

    # Traverse data_loader
    for i, batch in enumerate(train_data_loader):
        print("{}:{}".format(i, batch))

# 0:[tensor([1, 1, 1, 1, 1, 1, 1, 1, 1, 1]), tensor([[1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000,
#          1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000,   15,   17,   16,
#          1000,    1, 1000, 1000,  147, 1000,   29, 1000,   55, 1001, 1001, 1001,
#          1001, 1001, 1001, 1001, 1001, 1001, 1001, 1001, 1001, 1001, 1001, 1001,
#          1001, 1001, 1001, 1001, 1001],
#         [1000,  852, 1000,   74,  253, 1000, 1000, 1000, 1000,  119,   56,   21,
#   表示一个batch,这个batch有10个sequence,每个sequence有固定长度词向量，tensor([1, 1, 1, 1, 1, 1, 1, 1, 1, 1])表示10个sequence的label,17是序列中某个词的索引
