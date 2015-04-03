
# -*- coding:utf-8 -*-

#from Tkinter import *
import Tkinter, time, threading, random, Queue

def is_alph(x):
        if((ord(x) >= ord('a') and ord(x) <= ord('z'))\
        or (ord(x) >= ord('A') and ord(x) <= ord('Z'))):
                return(True)
        return(False)

def str_split(y = ''):
        l = len(y)
        i = 0
        all_words = []
        while(i < l):
                tmp = '' #保存""里的词
                tmp1 = ''#保存and, or 或者括号
                while(i < l and y[i] != '"'):
                        #把2个"号之间的词提取并保存起来
                        if(is_alph(y[i])):#如果是and或者or
                                tmp1 += y[i]
                                i += 1
                                while(i < l and is_alph(y[i])):
                                        tmp1 += y[i]
                                        i += 1
                                all_words.append([tmp1,1])#标号为1
                                tmp1 = ''
                        elif(y[i] == '('):
                                all_words.append(['(',2])
                                i += 1
                        elif(y[i] == ')'):
                                all_words.append([')',3])
                                i += 1
                        else:
                                i += 1
                i += 1

                while(i < l and y[i] != '"'):
                        tmp += y[i]
                        i += 1
                if(tmp != ''):
                        all_words.append([tmp,0]);
                i += 1
        return(all_words)


class MonitorGui(object):

        max_num = 100 # 通过gui获得的最大保存消息数
        filter_str = [] # 通过gui获得的过滤字符串
        filter_flag = 0# 通过gui获得的过滤标记

        def __init__(self, addr):
               
                self.filter_flag = 1
                ''' 子GUI根'''
                self.nroot = Tkinter.Tk()
                self.nroot.title(addr[0] + ':' + addr[1])

                ''' 标题信息'''
                self.lbl_title = Tkinter.Label(self.nroot, \
                                       text = '0 message has been saved.', \
                                       relief = Tkinter.GROOVE, width =60)

                self.lbl_title.pack()

                '''断开连接btn'''
                self.btn_disc = Tkinter.Button(self.nroot, text = 'Disconnect', width = 30, command = self.nroot.destroy)
                self.btn_disc.pack()
                
                self.fr_tm = Tkinter.Frame(self.nroot, width = 60, relief = Tkinter.GROOVE, borderwidth = 2)
                self.fr_tm.pack()

                self.fr_imf = Tkinter.Frame(self.fr_tm)
        
                self.lbl_imf = Tkinter.Label(self.fr_imf, width = 40)
                self.lbl_imf.pack(side = Tkinter.LEFT)
            
                Tkinter.Radiobutton(self.fr_imf, variable = self.filter_flag , value = 1, \
                            indicatoron = 1, text = 'Hide', command = self.get_filter_flag_hide).pack(side = Tkinter.LEFT)
                Tkinter.Radiobutton(self.fr_imf, variable = self.filter_flag , value = 0, \
                            indicatoron = 1, text = 'Show',command = self.get_filter_flag_show).pack(side = Tkinter.LEFT)
                
                #self.filter_flag.set(0)
                self.fr_imf.pack()
        
                '''过滤和保存数设置部分'''
                self.fr_ft = Tkinter.Frame(self.fr_tm, width = 60, relief = Tkinter.GROOVE, borderwidth = 2)
                self.fr_ft.pack()
                '''过滤'''
                self.lbl_key = Tkinter.Label(self.fr_ft, text = 'Keywords:')
                self.lbl_key.grid(row = 0, sticky = Tkinter.W)
                self.ent_filter = Tkinter.Entry(self.fr_ft, width = 40)
                self.ent_filter.grid(row = 0, column = 1, sticky = Tkinter.W)
        
                self.btn_filter = Tkinter.Button(self.fr_ft, text = "Filter", command = self.get_filter_str)
                self.btn_filter.grid(row = 0, column = 2, sticky = Tkinter.W)
                '''报文保存数量设置部分'''
                self.lbl_times = Tkinter.Label(self.fr_ft, text = 'Save Number:')
                self.lbl_times.grid(row = 1, sticky = Tkinter.W)
                self.ent_times = Tkinter.Entry(self.fr_ft)
                self.ent_times.grid(row = 1, column = 1, sticky = Tkinter.W)
        
                self.btn_times = Tkinter.Button(self.fr_ft, text = "Set  ", command = self.get_max_num)
                self.btn_times.grid(row = 1, column = 2, sticky = Tkinter.W)

                '''Disp标签'''
                self.lbl_msg = Tkinter.Label(self.nroot, text = "Disp:", width = 60)
                self.lbl_msg.pack()
                '''消息显示'''
                self.fr_msg = Tkinter.Frame(self.nroot, relief = Tkinter.GROOVE, width = 60)
                self.txt_msg = Tkinter.Text(self.fr_msg, height = 15, width = 60)
                self.scroll = Tkinter.Scrollbar(self.fr_msg, command = self.txt_msg.yview)
                self.txt_msg.configure(yscrollcommand = self.scroll.set)
                self.txt_msg.pack(side = Tkinter.LEFT)
                self.scroll.pack(side = Tkinter.RIGHT, fill = Tkinter.Y)
                self.fr_msg.pack()

                self.ent_times.insert(0, str(self.max_num))

                self.txt_msg.tag_config('a',foreground = 'red')
                self.txt_msg.tag_config('b',foreground = 'black')
        
        def get_max_num(self):
                self.max_num = int(self.ent_times.get())
        
        def get_filter_flag_hide(self):

                self.filter_flag = 1

        def get_filter_flag_show(self):

                self.filter_flag = 0

        def get_filter_str(self):

                self.filter_str = self.ent_filter.get()
                self.filter_str = str_split(self.filter_str)
                print self.filter_str
                s = []
                if_error = 0
                for i in range(0,len(self.filter_str)):
                        if(self.filter_str[i][1] == 1):
                                if(self.filter_str[i][0][0] == 'a' or self.filter_str[i][0][0] == 'A'):
                                        if(self.filter_str[i][0] != 'and' and self.filter_str[i][0] != 'And' and \
                                          self.filter_str[i][0] != 'aNd' and self.filter_str[i][0] != 'anD' \
                                        and self.filter_str[i][0] != 'ANd' and self.filter_str[i][0] != 'AnD' \
                                        and self.filter_str[i][0] != 'aND' and self.filter_str[i][0] != 'AND'):
                                                if_error = 1
                                                self.filter_str[i][0] = 'and'
                                        else:
                                                self.filter_str[i][0] = 'and'

                                elif(self.filter_str[i][0][0] == 'o' or self.filter_str[i][0][0] == 'O'):
                                        if(self.filter_str[i][0] != 'or' and self.filter_str[i][0] != 'Or' \
                                          and self.filter_str[i][0] != 'oR' and self.filter_str[i][0] != 'OR'):
                                                if_error = 1
                                                self.filter_str[i][0] = 'or'
                                        else:
                                                self.filter_str[i][0] = 'or'
                if(if_error == 1): 
                        self.lbl_imf['text'] = '关键字or或and有错，已自动补全'

                formular = ''
                for i in self.filter_str:
                        if(i[1] == 0):
                                formular += '1 '
                        else:
                                formular +=  i[0] + ' '
                print 'formular', formular
                try:
                        if(formular == ''):
                                self.filter_str = []
                                return

                        tmp = eval(formular)
                        print 'tmp:', tmp

                except:
                        # 弹出一个窗口说输入不正确，请重新输入
                        self.lbl_imf['text'] = '表达式有误，请重新输入'
                        self.filter_str = []
                        return
                if(if_error != 1):
                        self.lbl_imf['text'] = '表达式合法'

       # def run(self):
                #self.nroot.mainloop()
