
# -*- coding:utf-8 -*-

#from Tkinter import *
import Tkinter, time, threading, random, Queue
from client  import  Client
    
class MainGui(object):
    def __init__(self, master):#, master, queue, endCommand):
        #self.queue = queue

        self.master = master

        master.title("电信设备命令报文监视器v0.9 SauceForge");#题目
        self.lbl_title = Tkinter.Label(master, text = "Main")#题目标签
        self.lbl_title.pack()
        
        ''' addr'''
        self.fr_addr = Tkinter.Frame(master, relief = Tkinter.GROOVE, borderwidth = 2 )
        self.fr_addr.pack()
        self.lbl_ip = Tkinter.Label(self.fr_addr, text = 'IP:')
        self.lbl_ip.grid(row = 1, sticky = Tkinter.W)
        self.ent_ip = Tkinter.Entry(self.fr_addr, width = 35)
        self.ent_ip.grid(row = 1, column = 1, sticky = Tkinter.W)

        self.lbl_port = Tkinter.Label(self.fr_addr, text = 'Port:')
        self.lbl_port.grid(row = 1, column = 3, sticky = Tkinter.W)
        self.ent_port = Tkinter.Entry(self.fr_addr, width = 15)
        self.ent_port.grid(row = 1, column = 4, sticky = Tkinter.W)

        '''connect btn'''
        self.fr_btn = Tkinter.Frame(master)
        self.fr_btn.pack()
        self.btn_connect = Tkinter.Button(self.fr_btn, text = "Connect",command = self.connect_handler, width = 20)
        self.btn_connect.pack(side = Tkinter.LEFT)
        self.btn_quit = Tkinter.Button(self.fr_btn, text = "Quit", command = self.quit, width = 20)
        self.btn_quit.pack(side = Tkinter.LEFT)

        '''.日志'''
        self.lbl_log = Tkinter.Label(master, width = 58,relief = Tkinter.GROOVE, borderwidth = 2,
                                     text = "0 Connection has been Created!")
        self.lbl_log.pack()

        '''日志内容'''
        self.fr_log = Tkinter.Frame(master, borderwidth = 2)
        self.txt_log = Tkinter.Text(self.fr_log, height = 12, width = 55)
        self.scroll = Tkinter.Scrollbar(self.fr_log, command = self.txt_log.yview)
        self.txt_log.configure(yscrollcommand = self.scroll.set)
        self.txt_log.pack(side = Tkinter.LEFT)
        self.scroll.pack(side = Tkinter.RIGHT, fill = Tkinter.Y)
        self.fr_log.pack()

        '''ip, port 默认值设置'''
        self.ent_ip.insert(0,'127.0.0.1')
        self.ent_port.insert(0,'2012')

        self.__conter = 0

    def quit(self):
        self.master.quit()
        self.master.destroy()
        
    def connect_handler(self): #连接相应
            self.__mtime = time.strftime('[%Y/%m/%d %H:%M:%S]',time.localtime())
            self.txt_log.insert(Tkinter.END, self.__mtime + '[connect to]'\
                            + self.ent_ip.get() + ':' + self.ent_port.get() + '\n')
            self.__conter += 1
            self.lbl_log['text'] = str(self.__conter) + " Connection(es) has been Created!"

            #tmp_ngui = MonitorGui((self.ent_ip.get(), self.ent_port.get()))
            #tmp_ngui.run()

            # tmp_client = Client()
            tmp_client = Client((self.ent_ip.get(), self.ent_port.get()) )
            tmp_client.process()

