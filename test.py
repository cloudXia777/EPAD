# _*_coding: utf-8 _*_
# author    :14166
# DATA  : 20:40
# LAST MODIFIED BY :14166
# LAST MODIFIED BY  : 20:40

target_dir = 'C:\\Users\\14166\\Desktop\\result\\'
source_dir = 'C:\\Users\\14166\\Desktop\\0.18898_pointer_network_result\\'

import os

file_list = os.listdir(source_dir)

for i in file_list:
    if (int(i[:-4])>100) and (int(i[:-4])<=522):
        source = open(source_dir + i, 'r', encoding='utf-8')
        target = open(target_dir+str(int(i[:-4])+1)+'.txt','w',encoding='utf-8')
        data = source.readline()
        target.write(data)
        target.close()
        source.close()
    if i == '523.txt':
        source = open(source_dir + i, 'r', encoding='utf-8')
        target = open(target_dir+'101.txt', 'w', encoding='utf-8')
        data = source.readline()
        target.write(data)
        target.close()
        source.close()
    else:
        source = open(source_dir + i, 'r', encoding='utf-8')
        target = open(target_dir + i, 'w', encoding='utf-8')
        data = source.readline()
        target.write(data)
        target.close()
        source.close()

