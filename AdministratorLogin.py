# _*_coding: utf-8 _*_
# author    :西南交一枝花
# DATA  : 14:40
# LAST MODIFIED BY :西南交一枝花
# LAST MODIFIED BY  : 14:40
import tkinter
import utils as apputils
import tkinter.messagebox
from tkinter import *
from tkinter import ttk,Frame
from PIL import ImageTk
import PIL
from model.train import Train
from model.bio_tagger import *
from model.val import *
import os
import numpy as np

class Admin(Frame):
    def __init__(self,parent_frame):
        Frame.__init__(self,parent_frame)
        self.parent_frame = parent_frame
        self.ui()
    def ui(self):
        self.parent_frame.title('Administrator')
        self.parent_frame.iconbitmap('./logo.ico')
        self.img_png = PIL.Image.open("Admin.png")
        self.img = ImageTk.PhotoImage(image=self.img_png)
        self.label_img = tkinter.Label(self.parent_frame,image=self.img)
        self.label_img.pack(side=TOP,fill=X)
        self.statAnaly = Button(self.parent_frame,text='Statistical Analysis',font=("Arial",13),command=self.SA)
        self.statAnaly.pack(side=LEFT,anchor=SW,expand=YES,pady=5,padx=5)
        self.predict = Button(self.parent_frame, text='Predict', font=("Arial", 13), command=self.Predict)
        self.predict.pack(side=LEFT,anchor=S,expand=YES,pady=5,padx=5)
        self.report = Button(self.parent_frame, text='Training   Model', font=("Arial", 13),command=self.Train)
        self.report.pack(side=RIGHT,anchor=SE,expand=YES,pady=5, padx=5)
    def Predict(self):
        self.win1 = Toplevel(self.parent_frame)
        self.win1.title("Predict Module")
        apputils.setCenteredDisply(self.win1, 440, 350)
        Label(self.win1, text='Predict_Dir: \'./EPAD/model/test_data\'', font=('Arial', 12)).grid(row=0, column=0, sticky=W,
                                                                                        columnspan=3)
        self.text = Text(self.win1, font=('Arial', 7))
        self.text.grid(row=1, column=0, columnspan=3, rowspan=7, padx=12, sticky=E + W + S + N)
        self.sb = Scrollbar(self.win1)
        self.sb.grid(row=1, column=3, rowspan=7, padx=0, sticky=E + W + N + S)
        self.text['yscrollcommand'] = self.sb.set
        self.sb['command'] = self.text.yview
        data = open('./model/parameter','r',encoding='utf-8')
        parameters = data.readlines()[0].strip().split('\t')
        # [embed,lstm_dim,optimizer,lr,gpu,gpu_no]
        if len(parameters)==5:
            parameters.append(0)
        val(int(parameters[0]),int(parameters[1]),parameters[2],float(parameters[3]),parameters[4],parameters[5],self.text)
    def SA(self):
        dirs = apputils.Check()
        ann_num = [len(os.listdir('./Multi_Annotator/' + i)) for i in dirs]
        if len(set(ann_num)) != 1:
            tkinter.messagebox.showerror('错误', '标注者文件数目不同')
        # 不确定实体统计
        Annotator_num = len(dirs)
        File_num = list(ann_num)[0]
        uncertain_matrix = np.ones((File_num+1,Annotator_num+1))
        certain_matrix = np.ones((File_num+1,Annotator_num+1))
        for idy in range(Annotator_num):
            files = os.listdir('./Multi_Annotator/' + dirs[idy])
            for idx in range(len(files)):
                tmp1, tmp2 = apputils.getNum(path='./Multi_Annotator/' + dirs[idy] + '/' + files[idx])
                uncertain_matrix[idx][idy] = tmp1
                certain_matrix[idx][idy] = tmp2
        # 统计sum
        for idy in range(Annotator_num):
            temp1 = 0
            temp2 = 0
            for idx in range(File_num):
                temp1 += uncertain_matrix[idx][idy]
                temp2 += certain_matrix[idx][idy]
            uncertain_matrix[File_num][idy] = temp1
            certain_matrix[File_num][idy] = temp2
        # 求mean
        for idx in range(File_num):
            temp1 = 0
            temp2 = 0
            for idy in range(Annotator_num):
                temp1 += uncertain_matrix[idx][idy]
                temp2 += certain_matrix[idx][idy]
            uncertain_matrix[idx][Annotator_num] = int(temp1 / Annotator_num)
            certain_matrix[idx][Annotator_num] = int(temp2 / Annotator_num)
        file_list = os.listdir('./Multi_Annotator/' + dirs[0])
        un_list_matrix = apputils.Matrix2List(uncertain_matrix)
        cer_list_matrix = apputils.Matrix2List(certain_matrix)
        self.ChildWindow(dirs, file_list, un_list_matrix,cer_list_matrix)
    def ChildWindow(self,dirs,file,un_matrix,cer_matrix):
        '''

        :param dirs:
        :param file:
        :param un_matrix: 不确定标注2D列表
        :param cer_matrix: 确定标注2D列表
        :return:
        '''
        win2 = Toplevel(self.parent_frame)
        win2.title("Statistics")
        title = 'Uncertain/Certain'
        AVGE = 'AVGE'
        self.table = ttk.Treeview(win2, show="headings", columns=[title]+dirs+[AVGE])  # 列数 是否显示表头
        self.table.heading(title,text=title,anchor=CENTER)
        self.table.column(title,anchor=CENTER)
        for ann in dirs:
            self.table.heading(ann,text=ann,anchor=CENTER)
            self.table.column(ann,anchor=CENTER)
        self.table.heading(AVGE,text=AVGE,anchor=CENTER)
        self.table.column(AVGE,anchor=CENTER)

        self.table.pack(side=TOP,fill=BOTH)
        self.vbar = Scrollbar(self, orient=VERTICAL, command=self.table.yview)
        self.vbar.pack(side=RIGHT,fill=Y)
        self.table.configure(yscrollcommand=self.vbar.set)
        coverage = self.coverage_matrix(un_matrix,cer_matrix)
        print(coverage)
        for idx in range(len(file)):
            self.table.insert("",idx,values=[file[idx]]+coverage[idx])
        self.table.insert("",len(file),values=['Sum']+coverage[len(file)])
    def coverage_matrix(self,matrix1,matrix2):
        coverage = []
        sum1 = 0
        sum2 = 0
        for idx in range(len(matrix1)):
            line_list = []
            for idy in range(len(matrix1[0])):
                # 最后一行最后一列有些特殊     matrix1_sum/matrix2_sum
                if (idx == len(matrix1) - 1) and (idy != len(matrix1[0])-1):
                    sum1 += matrix1[idx][idy]
                    sum2 += matrix2[idx][idy]
                    temp2 = str(matrix1[idx][idy]) + '/' + str(matrix2[idx][idy])
                elif (idx == len(matrix1) - 1) and (idy == len(matrix1[0])-1):
                    temp2 = str(sum1)+'/'+str(sum2)
                else:
                    temp2 = str(matrix1[idx][idy])+'/'+str(matrix2[idx][idy])
                line_list.append(temp2)
            coverage.append(line_list)
        return coverage
    def Train(self):
        self.win2 = Toplevel(self.parent_frame)
        self.win2.title("Training Model Module")
        # apputils.setCenteredDisply(self.win2, 600, 400)
        Label(self.win2,text='Model:BiLSTM+CRF',background='lightblue',font=('Arial',15)).grid(row=0,column=0,sticky=W,
                                                                                      columnspan=2)
        Label(self.win2,text=' ',background='lightblue',font=('Arial',15)).grid(row=0,column=2,sticky=NSEW)
        Label(self.win2,text=' ',background='lightblue',font=('Arial',15)).grid(row=0,column=3,sticky=NSEW)
        Label(self.win2,text=' ',background='lightblue',font=('Arial',15)).grid(row=0,column=4,sticky=NSEW)
        Label(self.win2,text=' ',background='lightblue',font=('Arial',15)).grid(row=0,column=5,sticky=NSEW)

        Label(self.win2,text='Train_Dir: \'./model/train_data\'',font=('Arial',12)).grid(row=1,column=0,sticky=W,columnspan=3)
        Label(self.win2,text=' ',background='darkgray',font=('Arial',15)).grid(row=2,column=0,sticky=NSEW)
        Label(self.win2,text=' ',background='darkgray',font=('Arial',15)).grid(row=2,column=1,sticky=NSEW)
        Label(self.win2,text='   Configure',background='darkgray',fg='red',font=('Arial',15)).grid(row=2,column=2,sticky=NSEW)
        Label(self.win2,text=' ',background='darkgray',font=('Arial',15)).grid(row=2,column=3,sticky=NSEW)
        Label(self.win2,text=' ',background='darkgray',font=('Arial',15)).grid(row=2,column=4,sticky=NSEW)
        Label(self.win2,text=' ',background='darkgray',font=('Arial',15)).grid(row=2,column=5,sticky=NSEW)

        Label(self.win2,text='Embed_Dim:',font=('Arial',12)).grid(row=3,column=0,sticky=W)
        self.embed_dim = Entry(self.win2,width=6)
        self.embed_dim.grid(row=3,column=1,sticky=E)
        self.embed_dim.insert(END,'100')
        Label(self.win2, text='BiLSTM_Dim:', font=('Arial', 12)).grid(row=3, column=3,columnspan=1,sticky=W)
        self.BiLSTM_Dim = Entry(self.win2,width=6)
        self.BiLSTM_Dim.grid(row=3, column=4,columnspan=1,sticky=E)
        self.BiLSTM_Dim.insert(END,'100')
        Label(self.win2, text='Epochs:', font=('Arial', 12)).grid(row=4, column=0,sticky=W)
        self.epochs = Entry(self.win2,width=6)
        self.epochs.grid(row=4, column=1,sticky=E)
        self.epochs.insert(END,'80')
        Label(self.win2, text='Batches:', font=('Arial', 12)).grid(row=4, column=3, columnspan=1,sticky=W)
        self.batch = Entry(self.win2,width=6)
        self.batch.grid(row=4, column=4, columnspan=1,sticky=E)
        self.batch.insert(END,'400')
        Label(self.win2, text='ES_Patience:', font=('Arial', 12)).grid(row=5, column=0, sticky=W)
        self.patience = Entry(self.win2, width=6)
        self.patience.grid(row=5, column=1, sticky=E)
        self.patience.insert(END,'5')
        Label(self.win2, text='Val_Split:', font=('Arial', 12)).grid(row=5, column=3, columnspan=1, sticky=W)
        self.val_split = Entry(self.win2, width=6)
        self.val_split.grid(row=5, column=4, columnspan=1, sticky=E)
        self.val_split.insert(END,'0.2')
        Label(self.win2, text='Optimizer:', font=('Arial', 12)).grid(row=6, column=0, sticky=W)
        comvalue1 = tkinter.StringVar()
        self.list1 = ttk.Combobox(self.win2, width=6,textvariable=comvalue1)
        self.list1.grid(row=6, column=1, sticky=E)
        self.list1['values'] = ("sgd","adam")
        Label(self.win2, text='Learning_rate:', font=('Arial', 12)).grid(row=6, column=3, columnspan=1, sticky=W)
        self.lr = Entry(self.win2, width=6)
        self.lr.grid(row=6, column=4, columnspan=1, sticky=E)
        self.lr.insert(END,'0.001')
        Label(self.win2, text='GPU:', font=('Arial', 12)).grid(row=7, column=0, sticky=W)
        comvalue2 = tkinter.StringVar()
        self.list2 = ttk.Combobox(self.win2, width=6, textvariable=comvalue2)
        self.list2.grid(row=7, column=1, sticky=E)
        self.list2['values'] = ("ON", "OFF")
        Label(self.win2, text='GPU No :', font=('Arial', 12)).grid(row=7, column=3, columnspan=1, sticky=W)
        self.gpu_no = Entry(self.win2, width=6)
        self.gpu_no.grid(row=7, column=4, columnspan=1, sticky=E)

        Label(self.win2, text=' ', background='darkgray', font=('Arial', 15)).grid(row=8, column=0, sticky=NSEW)
        Label(self.win2, text=' ', background='darkgray', font=('Arial', 15)).grid(row=8, column=1, sticky=NSEW)
        Label(self.win2, text='Status', background='darkgray',fg='red',font=('Arial',15)).grid(row=8, column=2 ,sticky=NSEW)
        Label(self.win2, text=' ', background='darkgray', font=('Arial', 15)).grid(row=8, column=3, sticky=NSEW)
        Label(self.win2, text=' ', background='darkgray', font=('Arial', 15)).grid(row=8, column=4, sticky=NSEW)
        Label(self.win2, text=' ', background='darkgray', font=('Arial', 15)).grid(row=8, column=5, sticky=NSEW)
        self.status = Label(self.win2, text='*****Inital*****', fg='black', font=('Arial', 15))
        self.status.grid(row=10, column=2, sticky=NSEW)
        self.acc = Label(self.win2, text='  ', fg='black', font=('Arial', 15))
        self.acc.grid(row=11, column=2,columnspan=2,sticky=NSEW)
        Button(self.win2,text='Start',font=('Arial', 16),command=self.train).grid(row=12  ,rowspan=2,column=0,sticky=SW,ipadx=5,ipady=5)
        Button(self.win2,text='Quit',font=('Arial', 16),command=self.quit1).grid(row=12,rowspan=2,column=5,sticky=SE,ipadx=5,ipady=5)
    def quit1(self):
        self.win2.destroy()
    def train(self):
        embed_dim = int(self.embed_dim.get())
        lstm_dim = int(self.BiLSTM_Dim.get())
        batchs = int(self.batch.get())
        epochs = int(self.epochs.get())
        patience = int(self.patience.get())
        val_split = float('%.2f'%float(self.val_split.get()))
        optimizer = self.list1.get()
        lr = float(self.lr.get())
        gpu = self.list2.get()
        gpu_no = self.gpu_no.get()
        # print(embed_dim, lstm_dim, batchs, epochs, patience, val_split, optimizer, lr, gpu, gpu_no)
        train_new_path = './model/train_data/'
        self.acc["text"] = 'BIO Tagging'
        train = Train(embed_dim, lstm_dim, batchs, epochs, patience, val_split, optimizer, lr, gpu, gpu_no,self.status,self.acc)
        data = open('./model/parameter','w',encoding='utf-8')
        data.write(str(embed_dim)+'\t'+str(lstm_dim)+'\t'+str(optimizer)+'\t'+str(lr)+'\t'+gpu+'\t'+gpu_no)
        data.close()
        BIOtag(train_new_path)
        self.acc["text"] = 'BIO Finished'
        self.status["text"] = '****Training***'
        train.begin_train()

if __name__=='__main__':
    window = tkinter.Tk() # new frame
    apputils.setCenteredDisply(window, 500, 300)
    app = Admin(window)  # initial the UI
    mainloop()