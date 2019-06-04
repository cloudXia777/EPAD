# _*_coding: utf-8 _*_
# author    :西南交一枝花
# DATA  : 19:03
# LAST MODIFIED BY :西南交一枝花
# LAST MODIFIED BY  : 19:03

def getNum(path):
    data = open(path,'r',encoding='utf-8')
    lines = data.readlines()
    certain_num = 0
    uncertain_num = 0
    for line in lines:
        line = line.strip().split('\t')
        if line[4]=='certain':
            certain_num+=1
        else:
            uncertain_num+=1
    return uncertain_num,certain_num