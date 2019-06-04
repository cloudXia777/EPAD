# -*- coding: utf-8 -*-
# @Time    : 2018/10/23 17:09
# @Author  : ZOE
# @File    : train_vec.py
# @Software: PyCharm
import os
from gensim.models import word2vec

source_path = os.getcwd()
data_path=source_path+'/data/'
train_new_path=source_path+'/data/train_new/'
test_new_path=source_path+'/data/test_new/'
def deal_data():
        outfile=open('./data/text.txt','w',encoding='utf-8')
        document_file = os.listdir(train_new_path)
        document_file = sorted(document_file, key=lambda x: int(x.split('.')[0]))
        for index_file in range(0, len(document_file), 2):
                ori_data = open(train_new_path+ document_file[index_file + 1], 'r', encoding='UTF-8')  # 原始文本
                outfile.write(ori_data.read()+'\n')
        document_file1 = os.listdir(test_new_path)
        document_file1 = sorted(document_file1, key=lambda x: int(x.split('.')[0]))
        for index_file in range(0, len(document_file1)):
                ori_data = open(test_new_path+ document_file1[index_file], 'r', encoding='UTF-8')  # 原始文本
                outfile.write(ori_data.read()+'\n')
        outfile.close()

def get_vec():
        vec_out= data_path+ 'vec.txt'
        text=open(data_path+'text.txt','r',encoding='utf-8')
        model1=word2vec.Word2Vec(text, size=100,min_count=1)

        # model.save(outp1)
        model1.wv.save_word2vec_format(vec_out, binary=False)
# deal_data()
get_vec()
