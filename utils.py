# _*_coding: utf-8 _*_
# author    :14166
# DATA  : 9:04
# LAST MODIFIED BY :14166
# LAST MODIFIED BY  : 9:04
import os
import tkinter.messagebox
from tkinter import *
def setCenteredDisply(window, width, height):
    '''
    设置窗口大小 并将串口居中显示
    :param window: window object
    :param width: set the width of window
    :param height: set the height of window
    :return:
    '''
    # get screen width
    ww = window.winfo_screenwidth()
    # get screen height
    hw = window.winfo_screenheight()
    x = (ww - width) / 2
    y = (hw - height) / 2
    window.geometry("%dx%d+%d+%d" % (width, height, x, y))
def max_Forward_Match_English(content,dic, row):
    '''
    首先分行、分句
    :param content:  一篇文章
    :param dic: 已包含的此表
    :return: 返回单词及其id位置   不然无法回显
    '''
    dic = dic[0].strip().split()
    lines = content.strip().split('\n')
    words = []
    index = []
    for _idx, line in enumerate(lines):
        chars = line.strip().split() # 一行文本以空格分离
        for _i, w in enumerate(chars, 1):
            if w in dic:
                words.append(w)
                index.append((int(row) + _idx, _i))
    return words, index
def get_pre_ann(file_path):
    file = open(file_path,'r',encoding='utf-8')
    lines = file.readlines()

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
def Matrix2List(matrix):
    '''
    将矩阵转为二维列表
    :param matrix:
    :return: 二维列表
    '''
    list_matrix = []
    for idx in range(matrix.shape[0]):
        line = []
        for idy in range(matrix.shape[1]):
            line.append(matrix[idx][idy])
        list_matrix.append(line)
    return list_matrix
def Check():
    if not os.path.exists('./Multi_Annotator'):
        os.mkdir('./Multi_Annotator')
    dirs = os.listdir('./Multi_Annotator')
    for i in dirs:
        if os.path.isfile('./Multi_Annotator/'+i):
            tkinter.messagebox.showerror('错误','“Multi_Annotator”包含非法文件')
    return dirs
if __name__=='__main__':
    str = 'i am here, hello i am here hello \n imd fjdkf am hello'
    word = ['hello']
    words,index = max_Forward_Match_English(str,word, 2)
    print(words)
    print(index)
