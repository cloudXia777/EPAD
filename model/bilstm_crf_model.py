from keras.models import Model
from keras.layers import *
from keras_contrib.layers import CRF
import keras

class BiLSTM_CRF_Model:
    def __init__(self,num_classes,num_steps,word_dict_size,embed_dim,bilstm_dim,optimizer,lr):
        self.num_steps =num_steps
        self.num_classes =num_classes
        self.word_dict_size=word_dict_size
        self.word_embed_size = embed_dim  #180, 只采用字向量时用200
        self.rnn_units=bilstm_dim
        self.optimizer = optimizer
        self.lr = lr

    def model(self):
        input_words = Input(shape=(self.num_steps,), name='input_words')
        word_embedding = Embedding(self.word_dict_size+1,self.word_embed_size ,mask_zero=True,embeddings_initializer='glorot_uniform',
                                 trainable=True,name='word_embedding_layer')(input_words)  ## 随机初始化字向量
        bilstm = Bidirectional(LSTM(self.rnn_units,return_sequences=True),name='BILSTM_layer')(word_embedding)
        crf = CRF(self.num_classes , sparse_target=True)
        output = crf(bilstm)

        model = Model(inputs=[input_words], outputs=[output])
        model.summary()
        if self.optimizer == 'adam':
            model.compile(keras.optimizers.adam(lr=self.lr), loss=crf.loss_function, metrics=[crf.accuracy])
        if self.optimizer=='sgd':
            model.compile(keras.optimizers.sgd(lr=self.lr), loss=crf.loss_function, metrics=[crf.accuracy])
        return model