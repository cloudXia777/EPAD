import numpy as np
import os,math
from collections import OrderedDict,Counter
from keras.preprocessing.sequence import pad_sequences
import pickle
import platform
from configparse import Config
import sys

maxlen=338  # 填充后的样本最大长度

def load_data():
    train,train_word = _parse_data(open('./model/train_all_tag.txt', 'rb'))
    word_counts = Counter(row[0].lower() for sample in train_word for row in sample)  #字符    .lower()
    word_vocab = [w for w, f in iter(word_counts.items())]  # 字典大小
    # get the tag
    conf = Config()
    ent_dict = conf.getConf('ENTITY')
    ent_list = [w for w in ent_dict.keys()]
    tags = []
    tags.append('O')
    for w in ent_list:
        tags.append('B-'+w.capitalize())
        tags.append('I-'+w.capitalize())
    # save initial config data  存储配置信息
    with open('./model/weights/config.pkl', 'wb') as output:
        pickle.dump((word_vocab,tags), output)
    train_word,train_y= _process_data(train_word,word_vocab,tags,maxlen)
    return train_word,train_y,word_vocab,tags

def _parse_data(path):
    #  in windows the new line is '\r\n\r\n' the space is '\r\n' . so if you use windows system,
    #  you have to use recorsponding instructions
    if platform.system() == 'Windows':
        split_text = '\r\n'
    else:
        split_text = '\n'
    string = path.read().decode('utf-8')
    data = [[row.split('\t') for row in sample.split(split_text)] for sample in string.strip().split(split_text + split_text)]  ##以\n\n断文章

    path.close()
    ##----以句号“。”为切分-------------------
    new_data = []
    new_chapter = []
    split_flag = False
    for chapter in data:
        for word in chapter:
            if word[0] in ['。']:
                new_chapter.append(word)
                split_flag = True
            else:
                new_chapter.append(word)
            if split_flag == True:
                new_data.append(new_chapter)
                new_chapter = []
                split_flag = False
        if len(new_chapter)>0:
            new_data.append(new_chapter)
            new_chapter = []
    len_list = [len(sent) for sent in new_data]
    len_sorted=sorted(len_list)
    print('the 99% len of sen is ：',len_sorted[math.floor(0.99*len(len_sorted))]) #144
    print('the max len is：',max(len(i) for i in new_data))  #338
    print('the num of sens is:{}'.format(len(new_data)))  #7804
    return data, new_data

def _process_data(train_word, word_vocab,tags, maxlen=None, onehot=False):
    if maxlen is None:
        maxlen = max(len(sen) for sen in train_word)
    word2idx =dict((word, idx) for idx, word in enumerate(word_vocab,2))
    word2idx['PAD'] = 0
    word2idx['UNK'] = 1  # add pad and unk to word2idx dict

    x_word = [[word2idx.get(word[0].lower(),1) for word in sen] for sen in train_word] # set id of word if not found return 1
    y_tags = [[tags.index(pair[1]) for pair in sen if len(pair)==2] for sen in train_word] # label tag
    x_word= pad_sequences(x_word, maxlen,value=0)  # left padding
    y_tags= pad_sequences(y_tags, maxlen, value=-1)  #左拼接-1
    if onehot:
        y_tags = np.eye(len(y_tags), dtype='float32')[y_tags] # 利用对角矩阵生成onehot
    else:
        y_tags = np.expand_dims(y_tags, 2)
    return x_word,y_tags

## 处理测试集data
def process_data(data, word_vocab):
    # 针对切分后的数据以标题进行切分
    new_data = []
    new_chapter = []
    split_flag = False
    for word in data:
        if word in ['。']:
            new_chapter.append(word)
            split_flag = True
        else:
            new_chapter.append(word)
        if split_flag == True:
            new_data.append(new_chapter)
            new_chapter = []
            split_flag = False
    if len(new_chapter) > 0:
        new_data.append(new_chapter)
    len_list = [len(sent) for sent in new_data]
    '''**********'''
    split_flag = False
    new_chapter = []
    new_data2 = []

    for i in range(len(new_data)):
        if len_list[i] > maxlen:
            for word in new_data[i]:
                if word[0] in [',', ';']:
                    new_chapter.append(word)
                    split_flag = True
                else:
                    new_chapter.append(word)
                if split_flag == True:
                    new_data2.append(new_chapter)
                    new_chapter = []
                    split_flag = False
            if len(new_chapter) <= maxlen and len(new_chapter) > 0:
                new_data2.append(new_chapter)
                new_chapter = []
            if len(new_chapter) > maxlen:
                h = int(len(new_chapter) / maxlen)
                for idx in range(0, h):
                    new_data2.append(new_chapter[idx * maxlen:(idx + 1) * maxlen])
                if h * maxlen < len(new_chapter):
                    new_data2.append(new_chapter[h * maxlen:])
        else:
            new_data2.append(new_data[i])

    word2idx = dict((word, idx) for idx, word in enumerate(word_vocab,2))
    x_word = [[word2idx.get(word.lower(),1) for word in sent] for sent in new_data2]

    length_list=[]  #
    for sent in x_word:
        length = len(sent)    #每句话的原始长度
        length_list.append(length)
    x_word_pad = pad_sequences(x_word, maxlen)  # left padding
    return x_word,x_word_pad,length_list

def get_test_data(fp):
    with open('./model/weights/config.pkl', 'rb') as input_:
        (word_vocab, tags) = pickle.load(input_)

    test_data = open(fp, 'r', encoding='UTF-8')  # 原始文本
    test_ori=test_data.readline()
    x_word, x_word_pad, length_list=process_data(test_ori,word_vocab)
    test_data.close()
    return x_word,x_word_pad,length_list


if __name__ == '__main__':
    load_data()
    # get_test_data('159_8.txt')