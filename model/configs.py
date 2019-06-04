import tensorflow as tf

FLAGS = tf.app.flags.FLAGS

# Data files
tf.app.flags.DEFINE_string("data_path", "data/", "Data directory")
tf.app.flags.DEFINE_string("embedding_file", "embedding.txt","Embedding file")
tf.app.flags.DEFINE_string("embedding_vocab", "word.txt","Embedding vocab file")
tf.app.flags.DEFINE_string("word_embedding_file", "vec.txt","Word embedding file")
tf.app.flags.DEFINE_string("train_file", "i2b2-80.train", "Training file")
tf.app.flags.DEFINE_string("test_file", "i2b2-20.test", "Test file")
tf.app.flags.DEFINE_string("log_file", 'out/log.txt', "Log file")
tf.app.flags.DEFINE_string("model_path", 'model/', "save model here")
tf.app.flags.DEFINE_string("out_path", 'out/', "save ouput result here")

# Model Hyperparameters
tf.app.flags.DEFINE_integer("maxlen",2000, "Max sentence length in train/test data")
tf.app.flags.DEFINE_integer("word_embed_size",100, "Word embedding size")
# tf.app.flags.DEFINE_integer("pos_embed_num",403, "Max position embedding number")
tf.app.flags.DEFINE_integer("search_size",75, "position search_size")
tf.app.flags.DEFINE_integer("pos_embed_size",5, "Position embedding size")
tf.app.flags.DEFINE_integer("filter_size", 3 , "Filter size")
tf.app.flags.DEFINE_integer("num_filters",64,"How many features a convolution op have to output") #CNN输出单元数
tf.app.flags.DEFINE_integer("num_hidden", 64,"Number of RNN's hidden layer output") #RNN输出单元数
tf.app.flags.DEFINE_integer("num_classes",9, "Number of relations") #关系类别数目
tf.app.flags.DEFINE_integer("block_size", 2, "Size of each residual block")
tf.app.flags.DEFINE_integer("num_sampled", 1, "Sampling value for NCE loss")
tf.app.flags.DEFINE_integer("num_layers", 4, "Number of CNN layers")

# Training Hyperparameters
tf.app.flags.DEFINE_integer("batch_size",64, "Batch size") #一次喂多少样本
tf.app.flags.DEFINE_integer("num_epoches", 20, "Number of training epoches")  #遍历数据的轮数，此时要把样本跑20遍
tf.app.flags.DEFINE_float("dropout_prob", 0.5, "Dropout prob.")  #dropout率
tf.app.flags.DEFINE_float("learning_rate", 1e-2, "Learning rate.") #学习率，1e-3
tf.app.flags.DEFINE_float("l2_reg_lambda", 0.0001, "regularization parameter") #正则化参数
tf.app.flags.DEFINE_float("margin", 1, "margin based loss function") #损失函数中的余量
tf.app.flags.DEFINE_float("grad_clipping", 10., "Gradient clipping.")
tf.app.flags.DEFINE_float("momentum", 0.99 , "Nestrov Momentum value")
tf.app.flags.DEFINE_float("grad_clip", 0.1, "Gradient Clipping limit")

FLAGS = tf.app.flags.FLAGS    #flags.FLAGS直接命名FLAGS，简化使用