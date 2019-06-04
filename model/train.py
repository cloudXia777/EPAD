import model.bilstm_crf_model as bilstm_crf_model
import os
import model.model_utils as model_utils
import numpy as np
from keras.callbacks import ModelCheckpoint,EarlyStopping
import tensorflow as tf

class Train():
    def __init__(self,embed_dim,lstm_dim,batchs,epoches,patience,val_split,optimizer,lr,gpu,gpu_no,status,acc):
        self.embed_dim = embed_dim
        self.lstm_dim = lstm_dim
        self.batchs = batchs
        self.epoches = epoches
        self.patience = patience
        self.val_split = val_split
        self.optimizer = optimizer
        self.lr = lr
        self.gpu = gpu
        self.gpu_no = gpu_no
        self.status = status
        self.acc = acc
    def begin_train(self):
        train_word, train_y, word_vocab, tags = model_utils.load_data()
        num_classes = len(tags)
        num_steps = model_utils.maxlen
        word_dict_size = len(word_vocab)
        num_sample = len(train_word)
        shuffle_indices = np.random.permutation(np.arange(num_sample))  # 重新洗牌
        Train_word = train_word[shuffle_indices]
        Train_y = train_y[shuffle_indices]
        if self.gpu == 'ON':
            config = tf.ConfigProto()
            config.gpu_options.allow_growth = True
            sess = tf.Session(config=config)
            os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
            os.environ['CUDA_VISIBLE_DEVICES'] = self.gpu_no

        bilstm = bilstm_crf_model.BiLSTM_CRF_Model(num_classes, num_steps, word_dict_size,self.embed_dim,self.lstm_dim,self.optimizer,self.lr)
        model = bilstm.model()
        self.train_keras_Bi_CRF_Model(model,Train_word,Train_y)
    def train_keras_Bi_CRF_Model(self,model,Train_word,Train_y):
        prev_weights_file = './model/weights/weights.h5'  # weights.{epoch:02d}-{val_loss:.2f}.hdf5
        weights_file = './model/weights/weights.h5'
        try:
            model.load_weights(prev_weights_file)
            print("Continue training")
        except Exception:
            print("New model")
        earlyStopping = EarlyStopping(monitor='val_loss', patience=self.patience, verbose=0, mode='auto')  #val_loss
        saveBestModel = ModelCheckpoint(filepath=weights_file, monitor='val_loss', verbose=0, save_best_only=True,
                                       save_weights_only=True, mode='auto')

        history = model.fit([Train_word],Train_y,batch_size=self.batchs, epochs=self.epoches,validation_split=self.val_split, initial_epoch=0, callbacks=[earlyStopping,saveBestModel])
        model.save('./model/weights/BILSTM_CRF.h5')
        self.status["text"] = '***Finish***'
        self.acc["text"] = 'Train Acc'+str(history.history["acc"][-1])
# if __name__=='__main__':
#     train_keras_Bi_CRF_Model(model, batchs, epochs, patience, val_split)
