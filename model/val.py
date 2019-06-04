import model.bilstm_crf_model as bilstm_crf_model
import model.model_utils as utils
import pickle
import os,sys,re
from collections import defaultdict
import tensorflow as tf
from configparse import Config

test_new_path='./model/test_data/'
test_tag_path='./model/test_tag/'
test_true_label_path='./model/test_true_label/'
test_label_path='./model/test_label/'

def val(embed_dim,lstm_dim,optimizer,lr,gpu,gpu_no,text):
    if gpu == 'ON':
        config = tf.ConfigProto()
        config.gpu_options.allow_growth = True
        sess = tf.Session(config=config)
        os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"  # see issue #152
        os.environ['CUDA_VISIBLE_DEVICES'] = gpu_no
    with open('./model/weights/config.pkl', 'rb') as input_:
        (word_vocab,tags) = pickle.load(input_)
    TAGS={}
    idx=0
    for i in tags:
        TAGS[idx]=i
        idx+=1
    conf = Config()
    ent_dict = conf.getConf('ENTITY')
    ent_list = [w for w in ent_dict.keys()]
    B_I_dict = {}
    for w in ent_list:
        B_I_dict['B-' + w.capitalize()] = 'I-' + w.capitalize()
    num_classes=len(tags)
    num_steps=utils.maxlen
    word_dict_size=len(word_vocab)
    model = bilstm_crf_model.BiLSTM_CRF_Model(num_classes,num_steps,word_dict_size,embed_dim,lstm_dim,optimizer,lr).model()
    predict(model,TAGS,word_vocab,text)
    get_label_text(B_I_dict)
def predict(model,TAGS,word_vocab,text):
    model.load_weights('./model/weights/weights.h5')
    document_file = os.listdir('./model/test_data/')
    document_file = [file for file in document_file if 'txt' in file]
    file_count = 1
    for file in document_file:
        x_word,x_word_pad,length_list=utils.get_test_data(os.path.join(test_new_path,file)) # get processed test file
        test_tag=open(test_tag_path+file,'w',encoding='utf-8')
        print('正在进行预测的文件：'+file)
        text.insert(str(file_count)+'.0','正在进行预测的文件：'+file+'\n')
        file_count+=1
        predict_result = model.predict([x_word_pad])
        tags_pre_list = []  # 预测标签列表
        for i in range(len(predict_result)):
            sent_tag_list=[]
            for j in range(len(predict_result[i])):  # 句子长度#
                idx=list(predict_result[i][j]).index(1)  # get index of label
                sent_tag_list.append(TAGS[idx])
            tags_pre_list.append(sent_tag_list)

        for i in range(len(tags_pre_list)):
            if length_list[i] <= len(tags_pre_list[i]):  # 句子小于填充长度 即填补0
                for j in range(len(tags_pre_list[i])-length_list[i],len(tags_pre_list[i])):
                    test_tag.write(word_vocab[x_word_pad[i][j]-2]+'\t'+tags_pre_list[i][j]+'\n')
            else:   #句子大于填充长度
                print('hello, val.py 83 line')
                for j in range(len(tags_pre_list[i])):
                    test_tag.write(word_vocab[x_word_pad[i][j]-2]+'\t'+tags_pre_list[i][j]+'\n')
                for j in range(len(tags_pre_list[i]),length_list[i]):  #在组织训练集时被省略的部分
                    test_tag.write(word_vocab[x_word[i][j]-2]+'\t'+'O'+'\n')

def get_label_text(B_I_dict):
    document_file = os.listdir(test_tag_path)
    #document_file = sorted(document_file, key=lambda x: int(x.split('.')[0]))
    for index_file in range(len(document_file)):
        T_id = 1  #实体标注序号
        tag_file=open(test_tag_path+document_file[index_file],'r',encoding='utf-8')
        label_file=open(test_label_path+document_file[index_file].split('.')[0]+'.ann','w',encoding='utf-8')
        data = []
        for line in tag_file.readlines():
            if line != '\n':
                data.append(line.strip('\n').split('\t'))  # 去除空行后的数据
        for i in range(len(data)):
            if data[i][1] in B_I_dict.keys():  # B-   出现
                ent_type = data[i][1].split('-')[1]
                ent_s = i  # 实体开始的位置
                if data[i + 1][1] == 'O':  # 单实体
                    ent_e = i + 1
                for k in range(i + 1, i + 30):  # backward 30 characters
                    if data[k][1] == B_I_dict[data[i][1]]:
                        continue
                    else:
                        ent_e = k
                        break
                ent_str=''
                for w in range(ent_s,ent_e):
                    ent_str+=data[w][0]
                label_file.write('T'+str(T_id)+'\t'+ent_type+' '+str(ent_s)+' '+str(ent_e)+'\t'+ent_str+'\n')
                T_id+=1
def eval():
    right_num_all=0
    pred_num_all=0
    true_num_all=0
    true_file = os.listdir(test_true_label_path)
    true_file = sorted(true_file, key=lambda x: int(x.split('.')[0]))
    for  index_file in range(len(true_file)):
        right_num = 0  # 预测对的实体个数
        pred_num = 0  # 预测出的实体个数
        true_num = 0  # 真实实体个数
        truefile = open(test_true_label_path + true_file[index_file], 'r', encoding='utf-8') ##真实实体文件
        predfile=open(test_label_path+ true_file[index_file], 'r', encoding='utf-8')  #预测实体文件
        true_data=truefile.read().split('\n')
        pred_data=predfile.read().split('\n')
        true_dict = defaultdict(list)
        for line in true_data:
            if line !='':
                true_num +=1
                true_num_all += 1
                ent_idx = line.split('\t')[1]
                ent_type = ent_idx.split()[0]
                ent_s = int(re.split('[ ;]',ent_idx)[1])
                ent_e = int(re.split('[ ;]',ent_idx)[-1])
                true_dict[ent_type].append([ent_s,ent_e])
        for line in pred_data:
            if line !='':
                pred_num +=1
                pred_num_all += 1
                ent_idx = line.split('\t')[1]
                ent_type = ent_idx.split()[0]
                ent_s = int(ent_idx.split()[1])
                ent_e = int(ent_idx.split()[2])
                for item in true_dict[ent_type]:
                    if ent_s>=item[0] and ent_e<=item[1]:
                        right_num +=1
                        right_num_all += 1

        ###————————————评测指标计算————————————
        P=right_num/pred_num  #准确率
        R=right_num/true_num  #召回率
        F=2*P*R/(P+R)   #F值
        print(true_file[index_file]+'准确率：{}   召回率：{}  F值：{}'.format(P,R,F))
        # sys.exit()
    P_all = right_num_all / pred_num_all  # 准确率
    R_all = right_num_all / true_num_all  # 召回率
    F_all = 2 * P_all * R_all / (P_all + R_all)  # F值
    print('所有测试文件： 准确率：{}   召回率：{}  F值：{}'.format(P_all, R_all, F_all))



