import pickle
import os
from keras.models import Sequential
from keras.models import Model
from keras.layers import *
from keras_contrib.layers import CRF

class BiLSTM_CNN_CRF_Model:
    def __init__(self,num_classes,num_steps,word_dict_size,radical_dict_size,pinyin_dict_size,word_embeddings):
        self.num_steps =num_steps
        self.num_classes =num_classes #31
        self.word_dict_size=word_dict_size
        self.radical_dict_size=radical_dict_size
        self.pinyin_dict_size = pinyin_dict_size
        self.word_embed_size = 180
        self.radical_embed_size=10
        self.pinyin_embed_size = 10
        self.rnn_units=100
        self.word_embeddings=word_embeddings

    def model(self):
        input_words = Input(shape=(self.num_steps,), name='input_words')
        input_radical= Input(shape=(self.num_steps,), name='input_radical')
        input_pinyin = Input(shape=(self.num_steps,), name='input_pinyin')
        # word_embedding = Embedding(len(self.word_embeddings), len(self.word_embeddings[0]),weights=[self.word_embeddings],
        #                            trainable=True, mask_zero=True)(input_words) #使用预训练的字向量

        ##LSTM
        word_embedding=Embedding(self.word_dict_size+1,self.word_embed_size,embeddings_initializer='glorot_uniform',
                                 trainable=True,name='word_embedding_layer')(input_words)  ## 随机初始化字向量
        radical_embedding = Embedding(self.radical_dict_size+1, self.radical_embed_size, mask_zero=True,embeddings_initializer='glorot_uniform',
                                      trainable=True, name='radical_embedding_layer')(input_radical)  ## 随机初始化偏旁向量
        pinyin_embedding = Embedding(self.pinyin_dict_size+1, self.pinyin_embed_size, mask_zero=True,embeddings_initializer='glorot_uniform', trainable=True,
                                     name='pinyin_embedding_layer')(input_pinyin)  ## 随机初始化拼音向量
        concat_embedding = concatenate([word_embedding, radical_embedding, pinyin_embedding])  # 向量拼接
        bilstm = Bidirectional(LSTM(self.rnn_units, return_sequences=True),name='BILSTM_layer')(concat_embedding)  #dropout_W=0.1
        # bilstm_d = Dropout(0.1)(bilstm)
        half_window_size = 1
        ####CNN
        word_embedding_c=Embedding(self.word_dict_size+1,self.word_embed_size,embeddings_initializer='glorot_uniform',
                                 trainable=True,name='word_embedding_c_layer')(input_words)  ## 随机初始化字向量
        radical_embedding_c = Embedding(self.radical_dict_size+1, self.radical_embed_size,embeddings_initializer='glorot_uniform',
                                      trainable=True, name='radical_embedding_c_layer')(input_radical)  ## 随机初始化偏旁向量
        pinyin_embedding_c = Embedding(self.pinyin_dict_size+1, self.pinyin_embed_size,embeddings_initializer='glorot_uniform', trainable=True,
                                     name='pinyin_embedding_c_layer')(input_pinyin)  ## 随机初始化拼音向量
        concat_embedding_c = concatenate([word_embedding_c, radical_embedding_c, pinyin_embedding_c])  # 向量拼接
        paddinglayer = ZeroPadding1D(padding=half_window_size)(concat_embedding_c)
        conv = Conv1D(nb_filter=self.rnn_units, filter_length=(2 * half_window_size + 1), border_mode='valid',name='CNN_layer')(paddinglayer)
        # conv_d = Dropout(0.1)(conv)
        dense_conv = TimeDistributed(Dense(self.rnn_units))(conv)
        rnn_cnn_merge = concatenate([bilstm, dense_conv])
        dense = TimeDistributed(Dense(self.num_classes))(rnn_cnn_merge)
        crf = CRF(self.num_classes , sparse_target=True)
        output=crf(dense)

        model= Model(inputs=[input_words,input_radical,input_pinyin], outputs=[output])
        model.summary()
        model.compile('adam', loss=crf.loss_function, metrics=[crf.accuracy])
        return  model