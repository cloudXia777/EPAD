import os
from model.model_utils import *
from configparse import Config

train_new_path='./model/train_data/'
# label_dict need be modified , because the entity is Chinese.
conf = Config()
label_dict = conf.getConf('ENTITY_DESC')
# label_dict = {'身体部位':'Body','症状和体征':'Symptom','检查和检验':'Test','治疗':'Treatment','疾病和诊断':'Disease'}
def BIOtag(data_path):
    document_file = os.listdir(data_path)
    tag_all_file = open('./model/train_all_tag.txt', 'w', encoding='utf-8')
    document_file = [file for file in document_file if 'txt'in file]

    for file in document_file:
        ori_file = open(data_path + file, 'r', encoding='UTF-8')  # ori text
        label_file= open(data_path + file[:-3]+'ann', 'r', encoding='UTF-8')  # label text
        ori_data2=ori_file.readline()

        label_list = ['O'] * len(ori_data2)
        entity_list = label_file.read().split('\n')
        for entity in entity_list:
            if entity is not '':
                ent_index = entity.split('\t')
                ent_s = int(ent_index[1])
                ent_e = int(ent_index[2])+1
                ent_type=ent_index[3]
                ###——————————BIOS打标————————————
                # if ent_e-ent_s>1:  # 多字符实体
                #     label_list[ent_s]='B-'+ent_type
                #     for i in range(ent_s+1,ent_e):
                #         label_list[i]='I-'+ent_type
                # else:  #单实体
                #     label_list[ent_s] = 'S-' + ent_type
                ### ——————————BIO打标————————————
                label_list[ent_s] = 'B-' + label_dict[ent_type]
                for i in range(ent_s + 1, ent_e):
                    label_list[i] = 'I-' + label_dict[ent_type]
        for i in range(len(ori_data2)):
            tag_all_file.write(ori_data2[i]+'\t'+label_list[i]+'\n')
        tag_all_file.write('\n\n')
if __name__=='__main__':
    BIOtag(train_new_path)

