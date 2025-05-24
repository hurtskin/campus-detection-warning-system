import sys
import jieba
import torch
sys.path.append(r'opinionOnCampus\predict')
import os
from model import Model
from config import Config

class SentimentAnalyzer:
    def __init__(self):
        # 定义Config对象
        self.cfg = Config()

        # 加载词汇字典
        self.word_to_idx_path = r"./opinionOnCampus\data\dict.txt"
        self.word_to_idx = self.load_word_to_idx()

        # 确保字典中有 <UNK> 和 <PAD>
        self.word_to_idx.setdefault('<UNK>', len(self.word_to_idx))
        self.word_to_idx.setdefault('<PAD>', len(self.word_to_idx))

        # 加载停用词
        self.stopwords = self.load_stopwords()

        # 定义模型
        self.lstm_sentiment_cls = Model(self.cfg)
        self.lstm_sentiment_cls.to(self.cfg.devices)  # 'cuda' or 'cpu'

        # 加载预训练模型参数
        self.model_path = r"./opinionOnCampus\models\90.pth"
        self.load_model()

    def load_word_to_idx(self):
        word_to_idx = {}
        with open(self.word_to_idx_path, encoding='utf8') as f:
            for line in f.readlines():
                item = line.strip().split(',')
                word_to_idx[item[0]] = int(item[1].strip())
        return word_to_idx

    def load_stopwords(self):
        stopwords_path = r"./opinionOnCampus\data\stopwords.txt"
        if not os.path.exists(stopwords_path):
            raise FileNotFoundError(f"停用词文件未找到: {stopwords_path}")
        stopwords = set([line.strip() for line in open(stopwords_path, 'r', encoding='utf-8')])
        stopwords.update([" ", "\n"])  # 添加空格和换行符为停用词
        return stopwords

    def load_model(self):
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"模型文件未找到: {self.model_path}")
        self.lstm_sentiment_cls.load_state_dict(torch.load(self.model_path, map_location=self.cfg.devices))
        self.lstm_sentiment_cls.eval()  # 设置模型为评估模式

    def preprocess_text(self, text):
        jieba.load_userdict(self.word_to_idx_path)
        seg_list = jieba.cut(text, cut_all=False)
        seg_res = [word for word in seg_list if word not in self.stopwords]

        input_idx = [self.word_to_idx.get(word, self.word_to_idx['<UNK>']) for word in seg_res]

        max_vocab_size = self.lstm_sentiment_cls.embedding.num_embeddings
        input_idx = [idx if idx < max_vocab_size else self.word_to_idx['<UNK>'] for idx in input_idx]

        if len(input_idx) < self.cfg.pad_size:
            input_idx += [self.word_to_idx['<PAD>']] * (self.cfg.pad_size - len(input_idx))
        else:
            input_idx = input_idx[:self.cfg.pad_size]

        data = torch.tensor(input_idx).unsqueeze(0).to(self.cfg.devices)
        return data

    def predict_sentiment(self, text):
        data = self.preprocess_text(text)
        with torch.no_grad():
            pred = self.lstm_sentiment_cls(data)
            _, predicted_label = torch.max(pred, 1)
        return predicted_label.item()

    def sentiment_predict(self, text):
        '''
        情感预测函数，用于预测输入文本的情感倾向。
        '''
        print(text)
        sentiment_map = {0: "消极", 1: "积极"}  # 标签映射
        try:
            
            if text:
                sentiment = self.predict_sentiment(text)  
                return f"情感预测结果: {sentiment_map[sentiment]} ({sentiment})"
            
            else:
                return self.sentiment_predict_from_file()
        except Exception as e:
            print(f"发生错误: {e}")

    def sentiment_predict_from_file(self):
        sentiment_map = {0: "消极", 1: "积极"}  # 标签映射
        results = {}
        with open(r'./txt/testdata.txt', 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        for line in lines:
            sentiment = self.predict_sentiment(line)
            results[f"text: {line}"] = f"sentiment_code:{sentiment_map[sentiment]}"
        return results
