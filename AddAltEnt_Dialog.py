# _*_coding: utf-8 _*_
# author    :14166
# DATA  : 10:56
# LAST MODIFIED BY :14166
# LAST MODIFIED BY  : 10:56

from tkinter import *
import tkinter.font as tkFont
import utils
import tkinter.messagebox
from configparse import Config
class MyDialog():
    def __init__(self,parent,mode=None,entity=None):
        '''
        :param parent:
        :param mode: 添加实体 修改实体
        '''
        self.entity = entity
        super().__init__()
        self.top = Toplevel(parent)
        # top.attributes('-alpha',0.9) # fun attribute "transparent"
        if mode == 'add':
            self.top.title("添加实体")
        if mode == 'alter':
            self.top.title("修改实体")
        utils.setCenteredDisply(self.top, 400, 300)
        self.ft_1Title = tkFont.Font(family="宋体",size=11,weight=tkFont.BOLD)
        self.ft_2Title = tkFont.Font(family="宋体",size=9,weight=tkFont.BOLD)
        # l_class 从配置文件中读取
        self.conf = Config()
        ent_dict = self.conf.getConf('ENTITY')
        self.l_class = [ent for ent in ent_dict.keys()]
        self.v_class = StringVar()
        self.v_class.set(self.l_class)
        self.status = IntVar() # 标记复选框是否选中
        self.checkEntity = "certain" # 是否对实体确认
        self.entity_category = ''
        self.ui(self.top)
    def ui(self,top):
        for idx in range(0,8):
            top.columnconfigure(idx,weight=1)
        for idx in range(0,6):
            top.rowconfigure(idx,weight=1)
        Label(top,text=self.entity,font=self.ft_1Title,background='blue',fg='white').grid(row=0,column=0,columnspan=8,rowspan=1)
        # 下面设置对话框中要选择的类别 以及 不确定程度

        sb_category = Scrollbar(top)
        sb_category.grid(row=3,column=3,rowspan=2,sticky=E+W+N+S,padx=0)
        lb1 = Listbox(top,listvariable=self.v_class,yscrollcommand=sb_category.set,highlightcolor='blue',selectmode='SINGLE')
        lb1.grid(row=3, column=1,columnspan=2,rowspan=2,padx=3,sticky=E+W+N+S)
        Label(top,text="实体类型",font=self.ft_2Title,fg='light green',bg='dark green').grid(row=2,column=1,columnspan=2,sticky=E+W+N+S)
        Label(top,text="是否确定该实体",font=self.ft_2Title,fg='light green',bg='dark green').grid(row=2,column=4,columnspan=2,stick=E+W+N+S)
        sb_category.config(command=lb1.yview)

        v_checkButton = StringVar()
        v_checkButton.set("不确定的")
        self.checkFont = tkFont.Font(family="宋体",size=12,weight=tkFont.BOLD)
        Checkbutton(top,variable=self.status,textvariable=v_checkButton,font=self.checkFont,command=self.checkChange).grid(row=3,column=4,columnspan=3)

        Button(top,text="确 定",background='red',command=lambda :self.ok(lb1)).grid(row=5,column=1,columnspan=2,pady=2)
        Button(top,text="取 消",background='white',command=self.cancel).grid(row=5,column=4,columnspan=2,pady=2)
    def checkChange(self):
        if self.status.get()==1:
            self.checkEntity = 'uncertain'
        else:
            self.checkEntity = 'certain'
    def ok(self,lbl):
        try:
            indexs = lbl.curselection()
            index = int(indexs[0])
            self.entity_category = self.l_class[index]
            self.top.destroy()
        except:
            tkinter.messagebox.showerror("选择类别错误","请选择合法实体")
    def cancel(self):
        self.top.destroy()
def hello():
    d = MyDialog(root,mode='add',entity='hello')
    root.wait_window(d.top)
if __name__=='__main__':
    root = Tk()
    # root.geometry()
    Button(root,text="hello",command=hello).pack()
    root.update()
    mainloop()
