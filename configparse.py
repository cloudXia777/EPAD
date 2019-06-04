# _*_coding: utf-8 _*_
# author    :14166
# DATA  : 23:30
# LAST MODIFIED BY :14166
# LAST MODIFIED BY  : 23:30
import logging
import configparser
import os
logging.basicConfig(filename='./configs/log.log',format='[%(asctime)s-%(filename)s-%(levelname)s:%(message)s]',
                    level=logging.ERROR,filemode='a',datefmt='%Y-%m-%d%I:%M:%S %p')

class Config(object):
    def __init__(self):
        self.filename = './configs/Category.conf'
        self.cf = configparser.ConfigParser()
        self.cf.read(self.filename,encoding='UTF-8')
    def getConf(self,section):
        '''
        根据要获取的section 获取对应的字典
        :param section:
        :return: tmpdict
        '''
        tmpdict ={}
        if section not in self.cf.sections():
            logging.error('The section is not in configuration file')
        else:
            for keyname,value in self.cf.items(section):
                tmpdict[keyname] = value
        if len(tmpdict)!=0:
            return tmpdict
        else:
            return 'no sections'

    # 必须要将 实体和关系 都重新写 otherwise 会丢失另一个类别
    def setConf(self,section,config_dict):
        self.cf.remove_section(section)
        self.cf.add_section(section)
        for key in config_dict:
            if len(key) == 0:
                continue
            self.cf.set(section, key, str(config_dict[key]))
    def writeConf(self):
        with open(self.filename, 'w',encoding='utf-8') as f:
            self.cf.write(f)
        f.close()
if __name__=='__main__':
    conf = Config()
    print(conf.getConf('ENTITY'))

