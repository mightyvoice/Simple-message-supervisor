
# -*- coding:utf-8 -*-

import Tkinter
from maingui import MainGui

def  main():
        # 1. 实例化主窗口
        root = Tkinter.Tk()
        window = MainGui(root)
        root.mainloop()
        '''
        # 2. 每当点击连接新的电信设备就实例化一个client对象，
        # 然后创建线程跑client.process()
        client1 = client()
        client1.process()'''


if __name__ == '__main__':
        main()

