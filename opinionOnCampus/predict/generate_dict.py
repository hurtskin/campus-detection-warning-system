import jieba

with open("./data/weibo_senti_100k.csv", encoding='utf8') as f:
    # with open("./data/mini_weibo_senti.csv", encoding='utf8') as f:
    data_list = f.readlines()[1:]  # Read all data
with open("./data/stopwords.txt", encoding='utf8') as f:
    stop_words = f.readlines()  # Read all data

# 过滤停用词换行符
stop_words = [line.strip() for line in stop_words]
# Add ' ' and '\n', 停用词里加会被line.strip()过滤掉
stop_words.append(" ")
stop_words.append("\n")

# print(stop_words)
# The minimum threshold of word frequency，超过1的进行统计
min_seq = 1
topN = 3000  # The size of vod_dict is 1500

# Define vocabulary dictionary
voc_dict = {}
for item in data_list[:]:  # 控制读取多少行
    # Obtain labels
    label = item[0]
    # The first item is comma
    content = item[2:].strip()  # Strip the leading and heading space
    # jiaba Chinese segmentation
    seg_list = jieba.cut(content, cut_all=False)
    # Filter all stop words of the list
    seg_res = []

    for seg_item in seg_list:
        # Determine whether seg_item in the stop_words
        if seg_item not in stop_words:
            seg_res.append(seg_item)
            # Determine whether seg_item is in the vocabulary dictionary
            if seg_item in voc_dict.keys():
                voc_dict[seg_item] += 1  # Word frequency plus 1
            else:
                voc_dict[seg_item] = 1  # Add the word into the vocabulary dictionary
    # print(seg_res)  # Print all segmentation words list filtered by stop_words

# print(voc_dict)  # Print vocabulary dictionary

# 对词典词频进行排序，词频数过低，统一用一个embedding表示, voc_dict.items() return the tuple (key, value)
# key需要传入一个排序函数, reverse=True denotes sort by reverse order, [:topN]:put topN words in voc_list, means
# the max size of voc_list is topN.
voc_list = sorted([_ for _ in voc_dict.items() if _[1] > min_seq],
                  key=lambda x: x[1], reverse=True)[:topN]

# Number words in voc_list according to word frequency
voc_dict = {word_count[0]: idx for idx, word_count in enumerate(voc_list)}

# 字典以外的单词统一定义为UNK(unknown)
UNK = '<UNK>'
# 定义PAD用于序列填充，使所有sequence size 相等
PAD = '<PAD>'
# Put UNK and PAD in the end of voc_dict
voc_dict.update({UNK: len(voc_dict), PAD: len(voc_dict) + 1})
print(voc_dict)

# Create a file to store voc_dict
f_dict = open('./data/dict.txt', 'w', encoding='utf8')
for item in voc_dict.keys():
    f_dict.writelines("{},{}\n".format(item, voc_dict[item]))
f_dict.close()
