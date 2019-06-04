# _*_coding: utf-8 _*_
# author    :14166
# DATA  : 20:34
# LAST MODIFIED BY :14166
# LAST MODIFIED BY  : 20:34
from tkinter import *
from tkinter import ttk
import tkinter.messagebox
import utils
from configparse import Config
import re
class ConfigureEntRel_Dialog():
    def __init__(self,parent):
        super().__init__()
        self.top = Toplevel(parent)
        self.parent = parent
        self.top.title('Label&ShortcutKey Setting')
        utils.setCenteredDisply(self.top, 500, 400)
        self.row = 10
        self.column = 20
        # 可以通过tuple(list) 将列表转为tuple
        self.conf = Config()
        self.entdict = self.conf.getConf('ENTITY')
        if type(self.entdict) == str:
            self.entdict={}
        self.ui(self.top)
    def ui(self,top):
        self.top.iconbitmap('./logo.ico')
        for idx in range(0,self.column):
            top.columnconfigure(idx,weight=1)
        for idx in range(0,self.row):
            top.rowconfigure(idx,weight=1)
        Label(top,text="Label List").grid(row=2,column=0,rowspan=1,columnspan=8)
        self.cmb = ttk.Combobox(top)
        if len(self.entdict) != 0:
            entTup = tuple([keyname+'('+str(self.entdict[keyname])+')' for keyname in self.entdict.keys()])
            self.cmb['values'] = entTup
        self.cmb.grid(row=2,column=9,columnspan=9)
        self.cmb['state'] = 'readonly'
        if len(self.entdict) != 0:
            self.cmb.current(0)

        Label(top,text="Input label and shortcuts").grid(row=4,column=0,columnspan=8)
        self.entEnt = Entry(top)
        self.entEnt.grid(row=4,column=9,columnspan=9)

        # 创建两个按钮 用于更改配置
        delete = Button(top,text="Delete Selected",command=self.delete_entity)
        delete.grid(row=8,column=2)
        delete['width'] = 15
        add = Button(top,text="Add",command=self.addEntity)
        add.grid(row = 8,column=17)
        add['width'] = 15
    # 添加实体类别
    def addEntity(self):
        d_entity = self.entEnt.get()
        keyname = re.split('[:：]',d_entity)[0]
        value = re.split('[:：]',d_entity)[1]
        self.entEnt.delete(0,END)
        if d_entity in self.entdict.keys():
            tkinter.messagebox.showerror("Add Error", "Label Already Exists")
        else:
            self.entdict[keyname] = value
        self.update_com()
        self.toConfigure()
        # print(self.entEnt.get())
    # 删除选中实体类别
    def delete_entity(self):
        d_entity = self.cmb.get()
        d_entity = d_entity[:d_entity.find('(')]
        del self.entdict[d_entity]
        self.update_com()
        self.toConfigure()
    # 更新下拉列表
    def update_com(self):
        ent_tup = tuple([keyname+'('+str(self.entdict[keyname])+')' for keyname in self.entdict.keys()])
        self.cmb['values'] = ent_tup
    # 更新配置文件 此操作 再每次对实体类型进行操作后 都要进行
    def toConfigure(self):
        self.conf.setConf('ENTITY',self.entdict)
        self.conf.writeConf()
def hello():
    d = ConfigureEntRel_Dialog(root)
    root.wait_window(d.top)
if __name__ == '__main__':
    root = Tk()
    Button(root, text="hello", command=hello).pack()
    root.update()
    mainloop()

