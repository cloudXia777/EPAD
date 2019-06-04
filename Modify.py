# _*_coding: utf-8 _*_
# author    :西南交一枝花
# DATA  : 22:27
# LAST MODIFIED BY :西南交一枝花
# LAST MODIFIED BY  : 22:27
import os
import tkinter
import tkinter.filedialog as tkFileDialog
import tkinter.font as tkFont
import tkinter.messagebox
from tkinter import *
from tkinter.ttk import *
from configparse import Config
import utils
from AddAltEnt_Dialog import MyDialog
from ConfigureEntRel import ConfigureEntRel_Dialog
import re
import logging
logging.basicConfig(filename='./configs/log.log',format='[%(asctime)s-%(filename)s-%(levelname)s:%(message)s]',
                    level=logging.ERROR,filemode='a',datefmt='%Y-%m-%d%I:%M:%S %p')
class Modification():
    def __init__(self,parent_frame,dir_name,file_path):
        '''
        初始化系统参数
        :param parent: frame widget "parent=window"
        '''
        super().__init__()
        self.file_path = file_path   # 表示要修改的标注文件
        self.dir_name = dir_name   # 表示要修改的标注者
        self.top = Toplevel(parent_frame)
        utils.setCenteredDisply(self.top, 1000, 700)
        self.Version  = "EPAD-V1.0 Modify"
        self.currentPath = os.getcwd()
        self.fileName = ""
        self.textColumn = 7
        self.fntSize = 13
        self.allKey = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.pressCommand = {'a':"a1",
                             'b':"a2",
                             'c':"a3"}
        self.textFontSytle = "Times"
        self.textRow = 20
        self.no = 0 # 记录实体的序号，并且在treeview中记录插入位置

        self.conf = Config()
        self.recommendFlag1 = "ON"  # 最大前向匹配
        self.recommendFlag2 = "OFF"  # 深度学习
        self.recoEntity = '' # 设置当前要推荐的词语
        self.entity_list = []  # entity list # 实体类别
        self.ent_dict = self.conf.getConf('ENTITY') # 获得实体类别
        self.ent_list = [ent for ent in self.ent_dict.keys()] # !==[{'entity':,'pos':,},{},{},{}]    这个是类别列表
        self.selectColor = 'light salmon'  # 选中的颜色
        self.tagColor = 'lightgreen'  # 标记的颜色
        self.remColor = 'pink'  # 推荐的颜色
        self.preColor = 'purple' # 预标注的颜色
        self.onlylabel=''
        self.onlyhow=''
        self.initUI(self.top)
    def initUI(self,top):
        '''
        init the UI
        :return:
        '''
        top.title(self.Version)
        top.iconbitmap('./logo.ico')
        for idx in range(0,self.textColumn):
            top.columnconfigure(idx,weight = 2)
        for idx in range(0,24):
            top.rowconfigure(idx,weight=1)
        # 上方布局
        open_btn = Button(top,text="Open",command=self.onOpen,width=10)  # 打开文件
        open_btn.grid(row=0,column=0,ipady=5)
        open_btn.configure(state='disabled')
        RA_open_btn = Button(top,text="ReM1 SW",command=self.swNER1,width=10) # 第一种推荐方式
        RA_open_btn.grid(row=0,column=1,ipady=5)
        Label(top, text=self.recommendFlag1, foreground='red').grid(row=0, column=2)
        RA_close_btn = Button(top,text="ReM2 SW",width=10) # 第二种推荐方式
        RA_close_btn.grid(row=0,column=3,ipady=5)
        RA_close_btn.configure(state='disabled')
        Label(top, text=self.recommendFlag2, foreground='red').grid(row=0, column=4)
        set_sk_btn = Button(top,text="Ann ConF",width=10,command=self.sckSet)   #  快捷键配置
        set_sk_btn.grid(row=0,column=5,ipady=5)

        # 中间布局
        self.fnt = tkFont.Font(family=self.textFontSytle,size=self.fntSize,weight="bold",underline=0)
        self.text = Text(top,font=self.fnt,selectbackground=self.selectColor)
        self.text.grid(row=1,column=0,columnspan=self.textColumn,rowspan=self.textRow,padx=12,sticky=E+W+S+N)
        self.sb = Scrollbar(top)
        self.sb.grid(row=1,column=self.textColumn,rowspan=self.textRow,padx=0,sticky=E+W+N+S)
        self.text['yscrollcommand'] = self.sb.set
        self.sb['command'] = self.text.yview

        # 下方布局 设置实体列表显示
        self.table = Treeview(top,show="headings",columns=('NO','ENTITY','CLASS','UNCERTAIN')) # 列数 是否显示表头
        self.table.column('NO',anchor='center')
        self.table.column('ENTITY',anchor='center')
        self.table.column('CLASS',anchor='center')
        self.table.column('UNCERTAIN',anchor='center')
        self.table.heading("NO",text="NO")
        self.table.heading("ENTITY",text="ENTITY")
        self.table.heading("CLASS",text="CATEGORY")
        self.table.heading("UNCERTAIN",text="UNCERTAIN")
        self.table.grid(row=21,column=0,columnspan=self.textColumn+2,sticky=NSEW,rowspan=4)
        self.vbar = Scrollbar(top,orient=VERTICAL,command=self.table.yview)
        self.vbar.grid(row=21,column=self.textColumn+3,sticky=NSEW,rowspan=4)
        self.table.configure(yscrollcommand=self.vbar.set)
        self.table.bind('<Double-1>',self.tableClick)

        self.table.bind('<Control-q>',self.tableDelete) # 快捷删除预标注中的结果

        # 中间中间靠右布局
        export_Entity_btn = Button(top, text="Export", command=self.exportEntity,width=10)
        export_Entity_btn.grid(row=1, column=self.textColumn + 1, ipadx=5)
        import_Entity_btn = Button(top,text="Import",command=self.loadEntityFile,width=10)
        import_Entity_btn.grid(row=2,column=self.textColumn+1,ipadx=5)
        import_Entity_btn.configure(state='disabled')
        self.loadShortKey(top)  # 更新快捷键界面

        self.cursorName = Label(top,text="Cursor： ",foreground="Blue",font=(self.textFontSytle,12,"bold"))
        self.cursorName.grid(row=18,column=self.textColumn+1,pady=4)
        self.cursorIndex = Label(top,text=("Row: %s\nCol: %s"%(0,0)),foreground="red",font=(self.textFontSytle,12,"bold"))
        self.cursorIndex.grid(row=19,column=self.textColumn+1,pady=4)

        # 文本快捷键绑定  & table 快捷键修改
        self.text.bind('<ButtonRelease-1>', self.singleLeftClick)
        self.text.bind('<Button-3>', self.rightClick)  # 绑定 右击快捷键
        for key in self.ent_dict.keys():
            self.text.bind("<Control-Alt-" + self.ent_dict[key] + ">",
                           self.runSckAdaptor(self.runSCK, 'uncertain', key))
            self.text.bind("<Control-" + self.ent_dict[key] + ">",
                           self.runSckAdaptor(self.runSCK, 'certain', key))
            self.table.bind("<Control-Alt-" + self.ent_dict[key] + ">",
                            self.runSckAdaptor(self.tableAlter, 'uncertain', key))
            self.table.bind("<Control-" + self.ent_dict[key] + ">",
                            self.runSckAdaptor(self.tableAlter, 'certain', key))
        # 导入文本
        self.onOpen(self.file_path)
        # 导入已标注实体 （不确定位置有前后之分）
        self.loadEntityFile()
    def loadShortKey(self,top):
        ft1 = tkFont.Font(family='Arial',size=9)
        for i,w in enumerate(self.ent_dict.keys()):
            Label(top,text=w,font=ft1).grid(row=(3+i),column=self.textColumn+1)
            Label(top,text=self.ent_dict[w],font=ft1).grid(row=(3+i),column=self.textColumn+2)
    # 设置字体
    def setFont(self,value):
        _family = self.textFontSytle
        _size = value
        _weight = "bold"
        _underline = 0
        fnt = tkFont.Font(family=_family,size=_size,weight=_weight,underline=_underline)
        Text(self,font=fnt)
    def singleLeftClick(self,event):
        cursor_index = self.text.index(CURRENT)
        row_column = cursor_index.split('.')
        self.currentColumn = row_column[-1]
        cursor_text = ("Row：%s\nCol：%s"%(row_column[0],row_column[-1]))
        # print("row:%s col: %s"%(row_column[0],row_column[-1]))
        self.cursorIndex.config(text=cursor_text)
    # text 右击进行实体标注事件
    def rightClick(self,event):
        try:
            firstSelection_index = self.text.index(SEL_FIRST)
            begin = int(firstSelection_index.split('.')[-1])
            cursor_index = self.text.index(SEL_LAST)
            end = int(cursor_index.split('.')[-1])
            # content = self.text.get('1.0',"end-1c")
            content = self.text.selection_get()
            entity = "{0}【{1},{2}】".format(content,str(begin),str(end))
            if begin > end:
                tkinter.messagebox.showerror("OK","Invalid Entity")
            else:
                d = MyDialog(self, mode='add',entity=entity)
                self.wait_window(d.top)
                entity_dict = {'ENTITY':content,'POS':(begin,end),'CATEGORY':d.entity_category,'STATUS':d.checkEntity}
                if len(d.entity_category) != 0:
                    self.recoEntity = content
                    self.entity_list.append(entity_dict)
                    self.updateTable(self.entity_list)
                    self.setDisplayCorolor()
        except TclError:
            pass

    # 设置下拉列表鼠标左击按下事件
    def tableClick(self, event):
        self.text.tag_delete(self,'highlight')
        item = self.table.selection()[0]
        pos = re.split('\(|\)|,',self.table.item(item, 'values')[1])

        self.text.tag_config('highlight', background='red',foreground='white')
        self.text.tag_add('highlight', '1.' + str(pos[1]), '1.' + str(pos[2]))

    # 删除选中的一列
    def tableDelete(self,event):
        try:
            item = self.table.selection()[0]
            for i in self.entity_list:
                if self.table.item(item,'values')[1] == (i['ENTITY']+str(i['POS'])):
                    self.entity_list.remove(i)
                    self.text.tag_delete('TagEntity')
            self.text.config(state=NORMAL)
        except:
            logging.error('Table deletes error in function:tableDelete of Modify.py ')
        # self.text.tag_config('TagEntity', background=self.tagColor)
        # for sam in self.entity_list:
        #     self.text.tag_add('TagEntity', '1.' + str(sam['POS'][0]), '1.' + str(sam['POS'][1]))
        self.setDisplayCorolor()
        self.text.config(state=DISABLED)
        self.updateTable(self.entity_list)

    def tableAlter(self,event,how,label):
        try:
            entity = ''
            POS = ''
            item = self.table.selection()[0]
            for i in self.entity_list:
                if self.table.item(item,'values')[1] ==(i['ENTITY']+str(i['POS'])):
                    entity = i['ENTITY']
                    POS = i['POS']
                    self.entity_list.remove(i)
            if how==''and label=='':
                d = MyDialog(self, mode='alter', entity=entity)
                self.wait_window(d.top)
                entity_dict = {'ENTITY': entity, 'POS': POS, 'CATEGORY': d.entity_category, 'STATUS': d.checkEntity}
                if len(d.entity_category) != 0:
                    self.entity_list.append(entity_dict)
                    self.updateTable(self.entity_list)
            else:
                entity_dict = {'ENTITY': entity, 'POS': POS, 'CATEGORY': label, 'STATUS': how}
                self.entity_list.append(entity_dict)
                self.updateTable(self.entity_list)
        except:
            logging.error('Table alters error in function:tableAlter of Modify.py')
        self.setDisplayCorolor()
    # 更新实体表格
    def updateTable(self,list):
        self.clearTable()
        self.no=0
        for i in list:
            self.table.insert("",self.no,values=(self.no,i['ENTITY']+str(i['POS']),i['CATEGORY'],i['STATUS']))
            self.no = self.no+1
    # 清除表格实体
    def clearTable(self):
        x = self.table.get_children()
        for item in x:
            self.table.delete(item)
        self.no = 0
    # 再次重新显示所有标注实体
    # 在text中显示已经标注的实体颜色
    def setDisplayCorolor(self):
        self.text.config(state=NORMAL)
        if self.recommendFlag1 == "ON" and self.recoEntity!='':
            self.text.tag_config('RecEntity', background=self.remColor)
            try:
                new_words, index = utils.max_Forwar_Match(self.text.get('1.' + str(self.currentColumn), END),
                                                    [self.recoEntity])
            except:
                logging.error('Max_forwar_match error in function:setDisplayCorlor of Modify.py')
            for i in range(len(new_words)):
                self.text.tag_add('RecEntity', '1.' + str(index[i][0]+int(self.currentColumn)), '1.' + str(index[i][1]+int(self.currentColumn)))
                # self.setDisplayCorolor('1.' + str(index[0][1]), '1.' + str(index[i][1]), 'rec')
        self.text.tag_config('dpEntity', background=self.preColor,foreground='white')  # 覆盖的顺序是标记创建的顺序。
        self.text.tag_config('TagEntity', background=self.tagColor,foreground='black')  # 覆盖的顺序是标记创建的顺序。
        self.updateTable(self.entity_list)
        for sam in self.entity_list:
            self.text.tag_add('TagEntity', '1.' + str(sam['POS'][0]), '1.' + str(sam['POS'][1]))
        self.text.config(state=DISABLED)

    def onOpen(self,file_path):
        '''打开文件 并将内容显示到文本框内'''
        self.recoEntity = ''
        # 每次重新打开一个文件标注 清除预标注列表
        self.text.config(state=NORMAL)
        f1 = './model/test_data/'+file_path
        if f1!='':
            self.text.delete("1.0",END)
            text = self.readFile(f1)
            self.text.insert(END,text)
            self.setTitle(" "+f1)
            self.text.mark_set(INSERT,"1.0")
            self.no = 0
        self.clearTable() # 清空表格内容
        self.entity_list = [] # 清空实体内容
        # clear tag
        self.text.tag_delete(self,'TagEntity')
        self.text.tag_delete(self,'RecEntity')
        self.text.tag_delete(self,'dpEntity')
        self.text.tag_delete(self,'highlight')
        self.text.config(state=DISABLED) # set text state disable
        self.setDisplayCorolor()  # 首先 先显示预标注实体

    def setTitle(self,new_file):
        self.top.title(self.Version+new_file)
    def readFile(self,filename):
        '''读取文件 返回文件内容'''
        f  = open(filename,"rU",encoding='utf-8') # 以读方式打开，同时提供通用换行符支持
        text = f.read()
        text = text.replace("\n","")
        self.fileName = filename
        return text
    def autoLoadNewFile(self,fileName,newcursor_index):
        if len(fileName)>0:
            self.text.delete("1.0",END)
            text = self.readFile(fileName)
            self.text.insert("end-1c",text)
            self.setTitle("File: "+fileName)
            self.text.mark_set(INSERT,newcursor_index) # 标记
            self.text.see(newcursor_index)

    # 导出实体的显示框 并默认给定标注之后的文件名称
    def exportEntity(self):
        # print(self.fileName.strip().split('/')[-1][:-3])
        file_opt = options = {}
        options['defaultextension'] = '.ann'
        options['filetypes'] = [('entity files','.ann')]
        options['initialdir'] = ''.join(self.fileName.strip().split('/')[:-1])+'/'
        options['initialfile'] = self.fileName.strip().split('/')[-1][:-3]+'ann'
        options['title'] = "Save Entity File"
        checkItem = self.table.get_children()
        if not checkItem:
            tkinter.messagebox.showerror("Export Error", "No Entity Exists")
        else:
            entityFileName = tkFileDialog.asksaveasfilename(**file_opt)
            self.writeEntityFile(entityFileName)
            tkinter.messagebox.showinfo('提示','保存成功！')

    # 写出实体文件 如果要更改输出文件格式 在此修改
    def writeEntityFile(self,filename):
        # 获取所有已标注实体列表中的内容
        tmp_entity = self.getTableEntity()
        file = open(filename,'w',encoding='UTF-8')
        # print(''.join(str(self.entity_list[0]['POS'])))
        for i in tmp_entity:
            begin,end = i['POS']
            file.write(i['ENTITY']+'\t'+str(begin)+'\t'+str(end)+'\t'+i['CATEGORY']+'\t'+i['STATUS']+'\n')
        file.close()

    # 回显实体文件
    def loadEntityFile(self):
        entityFile = './Multi_Annotator/'+self.dir_name+'/'+self.file_path[:-3]+'ann'
        self.readEntityFile(entityFile)
    def readEntityFile(self,file):
        if os.path.exists(file):
            data = open(file,'r',encoding='utf-8')
            lines = data.readlines()
            self.entity_list = []
            certain_entity = []
            entity_dict = {}
            for i in lines:
                ent = i.strip().split('\t')
                # pos = ent[1].strip().split(' ')
                entity_dict['ENTITY'] = ent[0]
                entity_dict['POS'] = (int(ent[1]),int(ent[2]))
                entity_dict['CATEGORY'] = ent[3]
                if entity_dict['CATEGORY'] not in self.ent_list:
                    tkinter.messagebox.showerror("导入错误", "导入的实体类型与配置文件不匹配")
                entity_dict['STATUS'] = ent[4]
                if entity_dict['STATUS']=='uncertain':
                    self.entity_list.append(entity_dict)
                else:
                    certain_entity.append(entity_dict)
                entity_dict = {}
                self.setDisplayCorolor()
            self.entity_list = self.entity_list+certain_entity
            self.updateTable(self.entity_list)
        else:
            tkinter.messagebox.showerror('错误','请正确导入已标注实体文件')
    def quitFrame(self):
        self.top.destroy()
    # open recommend
    # 此处开始实体标注，两种标注形式，一种使用深度学习，一种使用最大前向匹配
    # 得到结果回显
    def swNER1(self):
        if self.recommendFlag1 == "ON":
            self.recommendFlag1 = "OFF"
        else:
            self.recommendFlag1 = "ON"
        Label(self, text=self.recommendFlag1, foreground='red').grid(row=0, column=2)
        if self.recommendFlag1=='OFF':
            self.text.tag_delete(self,'RecEntity')
    # 实体与关系配置
    def sckSet(self):
        d = ConfigureEntRel_Dialog(self)
        self.wait_window(d.top)
        self.ent_dict = self.conf.getConf('ENTITY')
        for key in self.ent_dict.keys():
            self.text.bind("<Control-Alt-" + self.ent_dict[key] + ">",
                           self.runSckAdaptor(self.runSCK,'uncertain',key))
            self.text.bind("<Control-" + self.ent_dict[key] + ">",
                           self.runSckAdaptor(self.runSCK,'certain',key))
            self.table.bind("<Control-Alt-" + self.ent_dict[key] + ">",
                           self.runSckAdaptor(self.tableAlter, 'uncertain', key))
            self.table.bind("<Control-" + self.ent_dict[key] + ">",
                           self.runSckAdaptor(self.tableAlter, 'certain', key))
        self.loadShortKey()     # 更新快捷键界面
    def runSckAdaptor(event,fun,how,label):
        '''事件处理函数的适配器，相当于中介'''
        return lambda event,fun=fun, how=how,label=label: fun(event,how,label)
    def runSCK(self,event,how,label):
        firstSelection_index = self.text.index(SEL_FIRST)
        begin = int(firstSelection_index.split('.')[-1])
        cursor_index = self.text.index(SEL_LAST)
        end = int(cursor_index.split('.')[-1])
        content = self.text.selection_get()
        entity_dict = {'ENTITY': content, 'POS': (begin, end), 'CATEGORY': label,
                       'STATUS': how}
        # print(entity_dict)
        self.recoEntity = content
        self.entity_list.append(entity_dict)
        self.updateTable(self.entity_list)
        self.clearTag()
        self.setDisplayCorolor()
        # except:
        #     print('except')
    def clearTag(self):
        self.text.tag_delete(self, 'TagEntity')
        # self.text.tag_delete(self, 'RecEntity')
        self.text.tag_delete(self, 'dpEntity')
        self.text.tag_delete(self, 'highlight')
    def getTableEntity(self):
        tmp_entity = []
        items = self.table.get_children()
        for i in items:
            tmp = self.table.item(i,'values')
            ent = re.split("\(|\)|,",tmp[1])
            ent_str = ent[0]
            ent_s = int(ent[1])
            ent_e = int(ent[2])
            label = tmp[2]
            how = tmp[3]
            dic = {'ENTITY':ent_str,'POS':(ent_s,ent_e),'CATEGORY':label,'STATUS':how}
            tmp_entity.append(dic)
        # print(tmp_entity)
        return tmp_entity
if __name__=='__main__':
    window = tkinter.Tk() # new frame
    setCenteredDisply(window, 1000, 700)
    app = Modification(window,'dfew','kdjfkd') # initial the UI
    mainloop()
