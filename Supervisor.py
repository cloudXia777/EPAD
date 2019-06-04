# _*_coding: utf-8 _*_
# author    :西南交一枝花
# DATA  : 22:11
# LAST MODIFIED BY :西南交一枝花
# LAST MODIFIED BY  : 22:11
import tkinter
import utils
from tkinter import *
import tkinter.messagebox
from tkinter import ttk
from PIL import Image,ImageTk
import numpy as np
import os
from Modify import Modification
class Supervisor(Frame):
    def __init__(self,parent_frame):
        Frame.__init__(self,parent_frame)
        self.parent_frame = parent_frame
        self.ui()
    def ui(self):
        self.parent_frame.title('Supervisor')
        self.img_png = Image.open("Super.png")
        self.parent_frame.iconbitmap('./logo.ico')
        self.img = ImageTk.PhotoImage(image=self.img_png)
        self.label_img = tkinter.Label(self.parent_frame,image=self.img)
        self.label_img.pack(side=TOP,fill=X)
        self.statAnaly = Button(self.parent_frame,text='Uncertain Statistics',font=("Arial",13),command=self.SA)
        self.statAnaly.pack(side=LEFT,expand=NO,pady=5,padx=5)
        Label(text='chart statistic')
        self.report = Button(self.parent_frame, text='Uncertain Modification', font=("Arial", 13),command=self.Modify)
        self.report.pack(side=RIGHT, expand=NO, pady=5, padx=5)

    def SA(self):
        dirs = utils.Check()
        ann_num = [len(os.listdir('./Multi_Annotator/'+i)) for i in dirs]
        if len(set(ann_num))!=1:
            tkinter.messagebox.showerror('错误','标注者文件数目不同')
        # 不确定实体统计
        Annotator_num = len(dirs)
        File_num = list(ann_num)[0]
        result_matrix = np.ones((File_num+1,Annotator_num+1))
        for idy in range(Annotator_num):
            files = os.listdir('./Multi_Annotator/'+dirs[idy])
            for idx in range(len(files)):
                tmp1,tmp2 = utils.getNum(path='./Multi_Annotator/'+dirs[idy]+'/'+files[idx])
                # print('./Multi_Annotator/'+dirs[idy]+'/'+files[idx])
                # print(tmp1,tmp2)
                result_matrix[idx][idy] = tmp1
        # 统计sum
        for idy in range(Annotator_num):
            temp = 0
            for idx in range(File_num):
                temp+=result_matrix[idx][idy]
            result_matrix[File_num][idy]=temp
        # 求mean
        for idx in range(File_num):
            temp = 0
            for idy in range(Annotator_num):
                temp+=result_matrix[idx][idy]
            result_matrix[idx][Annotator_num] = int(temp/Annotator_num)
        file_list = os.listdir('./Multi_Annotator/'+dirs[0])
        list_matrix = utils.Matrix2List(result_matrix)
        self.ChildWindow(dirs,file_list,list_matrix)

    def ChildWindow(self,dirs,file,matrix):
        '''
        显示统计信息
        :param dirs: 表示标注者
        :param file: 表示标注的文件名称
        :param matrix: 计算得到的矩阵
        :return:
        '''
        win2 = Toplevel(self.parent_frame)
        win2.title("Uncertain Statistics")
        # utils.setCenteredDisply(win2, 400, 300)
        title = 'Uncertain'
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
        total_sum = 0
        for idx in range(len(file)):
            self.table.insert("",idx,values=[file[idx]]+matrix[idx])
            total_sum+=matrix[len(file)][idx]
        total_avge = total_sum/len(file)
        # 计算矩阵的最后一格 样式为‘sum/avge’
        self.table.insert("",len(file),values=['Sum']+matrix[len(file)][:-1]+[str(total_sum)+'/'+str(total_avge)])

    def Modify(self):
        dirs = utils.Check()
        self.win2 = Toplevel(self.parent_frame)
        self.win2.title("Uncertain Modification")
        # utils.setCenteredDisply(win2, 600, 300)
        Label(self.win2, text='Select Annotator:').grid(row=0,sticky=W+E)
        self.v_annotator = StringVar()
        self.ann_combobox = ttk.Combobox(self.win2, width=9, textvariable=self.v_annotator)
        # dirs表示标注者集合
        self.ann_combobox['values'] = dirs
        self.ann_combobox.grid(row=0, column=1, sticky=E+W)
        self.ann_combobox.current(0)
        Button(self.win2, text='Query',command=self.Query).grid(row=0,column=2,sticky=E+W)



        # self.table3.bind('<Double-1>', self.tableClick)
    def Query(self):
        self.dir_name = self.ann_combobox.get()
        file_list = os.listdir('./Multi_Annotator/'+self.dir_name)
        file_num = len(file_list)
        result_matrix = np.ones((file_num,2))
        for idx in range(file_num):
            temp1,temp2 = utils.getNum('./Multi_Annotator/'+self.dir_name+'/'+file_list[idx])
            result_matrix[idx][0] = temp2
            result_matrix[idx][1] = temp1
        list_matrix = utils.Matrix2List(result_matrix)
        self.table3 = ttk.Treeview(self.win2, show="headings", columns=['File', 'Certain', 'Uncertain'])  # 列数 是否显示表头
        self.table3.column('File', anchor='center')
        self.table3.column('Certain', anchor='center')
        self.table3.column('Uncertain', anchor='center')
        self.table3.heading("File", text="File")
        self.table3.heading("Certain", text="Certain")
        self.table3.heading("Uncertain", text="Uncertain")
        self.table3.grid(row=1, column=0, columnspan=3, sticky=NSEW, rowspan=4)
        self.vbar = Scrollbar(self.win2, orient=VERTICAL, command=self.table3.yview)
        self.vbar.grid(row=1, column=4, sticky=NSEW, rowspan=4)
        self.table3.configure(yscrollcommand=self.vbar.set)
        for idx in range(file_num):
            self.table3.insert("", idx, values=[file_list[idx]] + list_matrix[idx])
        self.table3.bind("<Control-a>",self.ManModify)
    def ManModify(self,event):
        item = self.table3.selection()[0]
        file_name = self.table3.item(item, 'values')[0][:-3]+'txt'
        d = Modification(self,self.dir_name,file_name)
        self.wait_window(d.top)

if __name__=='__main__':
    window = tkinter.Tk() # new frame
    utils.setCenteredDisply(window, 600, 300)
    app = Supervisor(window)  # initial the UI
    mainloop()