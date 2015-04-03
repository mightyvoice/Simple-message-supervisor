
# -*- coding:utf-8 -*-

#from Tkinter import *
import Tkinter, time, threading, random, Queue
from threading import Thread
from monitorgui import MonitorGui
from connect import Connections

runState= 1;

class Client(object): #客户端窗口程序的主类

        connect_ins = None #连接实例
        window_ins = None #窗体实例
        write_file_name = None #写入数据的文件
        max_disp_num = 100 #最大显示数

        def __init__(self,address):
                self.address= address;
                self.connect_ins= Connections();
                self.write_file_name= self.address[0]+'-'+self.address[1]+'.txt';
                #print address ;

        def file_write(self):
                #self.write_file.writelines(self.connect_ins.dataReceived)
                global runState;
                while runState:
                        file= open(self.write_file_name,'w');
                        print self.write_file_name;
                        while len(self.connect_ins.dataReceived) > self.window_ins.max_num:
                                self.connect_ins.dataReceived.pop(0);
                        dataToBeWritten= [];
                        for items in self.connect_ins.dataReceived:
                                dataToBeWritten.append(items[0]+'  '+ items[1]+'\n');

                        file.writelines(dataToBeWritten);
                        file.close();
                        time.sleep(5);

                #print 'file_write has ended';
        
        def match_str(self, x):
                if(self.window_ins.filter_str == []):
                        return(1)
                formular = ''
                for i in self.window_ins.filter_str:
                        if(i[1] == 0):
                                if(x.find(i[0]) != -1):
                                        formular += '1 '
                                else:
                                        formular += '0 '
                        else:
                                formular += i[0] + ' '
                #print 'formular', eval(formular)
                #print 'self.window_ins.filter_flag.get()', self.window_ins.filter_flag
                if(self.window_ins.filter_flag== 1):
                        if(eval(formular) == 0):
                                return(1)
                        else:
                                return(0)
                else:
                        if(eval(formular) == 0):
                                return(0)
                        else:
                                return(1)

        def add_color_disp(self,x):
                if(x == None):
                        return
                interval = []
                if(self.window_ins.filter_str == []):
                        self.window_ins.txt_msg.insert(Tkinter.END, x+'\n','b')
                        return

                for i in self.window_ins.filter_str:
                        if(i[1] == 0):
                                l1 = x.find(i[0])
                                if(l1 != -1):
                                        interval.append([l1, l1 + len(i[0])])

                from operator import itemgetter 
                interval = sorted(interval, key=itemgetter(1))
                ans = []
                l = len(interval)
                ans.append(interval[0])
                j = 0
                for i in range(1, l):
                        if(ans[j][1] >= interval[i][0]):
                                ans[j][1] = interval[i][1]
                        else:
                                ans.append(interval[i])
                                j += 1

                sx = 0
                for i in ans:
                        self.window_ins.txt_msg.insert(Tkinter.END, x[sx:i[0]], 'b')
                        self.window_ins.txt_msg.insert(Tkinter.END, x[i[0]:i[1]], 'a')
                        sx = i[1]

                self.window_ins.txt_msg.insert(Tkinter.END, '\n', 'b')

        def mesg_process(self):
                while(1):
                        maxl = self.window_ins.max_num
                        print maxl,'sht'
                        l1 = len(self.connect_ins.dataReceived)
                        if(maxl < l1):
                                self.connect_ins.dataReceived = \
                                                self.connect_ins.dataReceived[l1-maxl:l1]
                        file_write_thread = Thread(target = self.file_write, args = ())
                        file_write_thread.start()
                        self.window_ins.txt_msg.delete(1.0, Tkinter.END)
                        self.window_ins.lbl_title['text'] = str(len( self.connect_ins.dataReceived)) +' message(s) has been saved'
                        for each in self.connect_ins.dataReceived:
                                if(self.match_str(each[1]) != 0):
                                        if(self.window_ins.filter_flag == 0):
                                                self.window_ins.txt_msg.insert(Tkinter.END, each[0] + \
                                                        '  ', 'b')
                                                self.add_color_disp(each[1])        
                                        else:
                                                self.window_ins.txt_msg.insert(Tkinter.END, each[0] + \
                                                        '  ' + each[1] + '\n', 'b')

                        time.sleep(1)
        


        def process(self):
                # 1. 开thread1 运行图形界面
                self.window_ins= MonitorGui(self.address)
                #thread1 = Thread(target = root.mainloop, args = ());
                #thread1.start()
                #root.mainloop()

                # 2. 开thread2 运行连接实例里的连接函数:connect_ins
                thread2 = Thread(target = self.connect_ins.connect,
                                args = (self.address[0],int(self.address[1]),True));
                thread2.start();

                # 3. 开thread3 运行mesg_process
                thread3 = Thread(target = self.mesg_process, args = ());
                thread3.start()

