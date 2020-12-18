# --- coding=utf-8 ---

import tkinter as tk
from tkinter import ttk
import random
from PIL import Image, ImageTk

# 自带取整的数
# 别问为什么,问就是之前忘记取整了
class Factor:
    def __init__(self, num):
        self.num = num

    def __rmul__(self, other):
        return int(self.num*other)

class Drawer:
    def __init__(self):
        self.chosenList = list(range(1,201))
        self.running = False
        self.decide = False
        self.mode = '三等奖'  # attention
        self.results = []

        # manage the style
        
        factor_x = Factor(1)
        factor_y = Factor(1)

        self.root = tk.Tk()
        self.root.geometry('%dx%d+%d+%d'%(1440*factor_x,360*factor_y,0*factor_x,280*factor_y))
        self.root.title('drawing')

        self.bg_label = tk.Label(self.root, width=280*factor_x, height=24*factor_y, bg='#ECf5FF')
        self.bg_label.place(anchor=tk.NW, x=0*factor_x, y=0*factor_y)

        self.var_roll = tk.StringVar(value='?')
        self.roll_label = tk.Label(self.root, textvariable=self.var_roll, font=("微软雅黑", 224), justify='left', \
                              anchor=tk.CENTER, width=4*factor_x, height=1*factor_y, bg='#BFEFFF', foreground='black')
        self.roll_label.place(anchor=tk.NW, x=446*factor_x, y=20*factor_y)

        self.var_state = tk.StringVar(value='- stand by me -', )
        self.state_label = tk.Label(self.root, textvariable=self.var_state, font=("微软雅黑", 18), justify='left', \
                               anchor=tk.CENTER, width=38*factor_x, height=1*factor_y, bg='#ECf5FF', foreground='red')
        self.state_label.place(anchor=tk.NW, x=490*factor_x, y=317*factor_y)

        self.start_button = tk.Button(self.root, text='开始黑幕', command=self.start, font=("微软雅黑", 18), \
                                 width=16*factor_x, height=2*factor_y, bg='#A8A8A8')
        self.start_button.place(anchor=tk.NW, x=1002*factor_x, y=20*factor_y)

        self.stop_button = tk.Button(self.root, text='停止黑幕', command=self.stop, font=("微软雅黑", 18), \
                                 width=16*factor_x, height=2*factor_y, bg='#A8A8A8')
        self.stop_button.place(anchor=tk.NW, x=1002*factor_x, y=70*factor_y)

        self.cancel_button = tk.Button(self.root, text='撤销', command=self.cancel, font=("微软雅黑", 18), \
                                 width=16*factor_x, height=2*factor_y, bg='#A8A8A8')
        self.cancel_button.place(anchor=tk.NW, x=1002*factor_x, y=250*factor_y)

        self.mode_label = tk.Label(self.root, text='奖项', height=2*factor_y, font=("微软雅黑", 18), \
                                   bg='#ECf5FF', foreground='black')
        self.mode_label.place(anchor=tk.NW, x=218*factor_x, y=12*factor_y)
        self.mode_box = ttk.Combobox(self.root, font=("微软雅黑", 18), \
                                     width=10*factor_x, textvariable=self.mode_label, state='readonly')
        self.mode_box['values'] = ('一等奖', '二等奖', '三等奖')
        self.mode_box.place(anchor=tk.NW, x=275*factor_x, y=20*factor_y)
        self.mode_box.current(2)

        self.result_box_frame = tk.Frame(self.root)
        self.result_box = tk.Listbox(self.root, width=8*factor_x, height=5, font=("微软雅黑", 36), \
                                     selectborderwidth=0, borderwidth=0, bg='#BFEFFF')
        self.result_box.place(anchor=tk.NW, x=229*factor_x, y=72*factor_y)
        self.result_box.delete(0,tk.END)

        self._img1 = ImageTk.PhotoImage(Image.open("hakase1.png"))
        self.img1 = tk.Label(self.root, image=self._img1, bg='#ECf5FF')
        self.img1.img = self._img1
        self.img1.place(anchor=tk.NW, x=1200*factor_x, y=5*factor_y)

        self._img2 = ImageTk.PhotoImage(Image.open("yuko1.png"))
        self.img2 = tk.Label(self.root, image=self._img2, bg='#ECf5FF')
        self.img2.img = self._img2
        self.img2.place(anchor=tk.NW, x=20*factor_x, y=50*factor_y)
        
        self.root.mainloop()

    def update(self):
        # 滚动
        self.var_roll.set(self.choose())
        if self.running:
            self.root.after(50, self.update)

    def int2str(self):
        # 格式化显示的字符串
        message = str(self.results[-1])
        if len(message) == 1:
            return message.center(22)
        elif len(message) == 2:
            return message.center(20)
        elif len(message) == 3:
            return message.center(18)

    def choose(self):
        # 抽奖就是简单的random
        if self.decide:
            self.results.append(random.choice(self.chosenList))
            self.result_box.insert(tk.END, self.int2str())
            self.decide = False
            return self.results[-1]
        else:
            return random.choice(self.chosenList)

    def start(self):
        # 开始
        if self.mode != self.mode_box.get():
            with open(self.mode+'.txt', 'w') as f:
                f.write(' '.join(map(str,self.results)))
                f.close()
            self.mode = self.mode_box.get()
            self.results = []
            self.result_box.delete(0,tk.END)  
        if not self.running:
            self.running = True
            self.update()

    def stop(self):
        # 停止
        if self.running:
            self.running = False
            self.decide = True

    def cancel(self):
        # 撤销
        if (not self.running) and self.results:
            self.results.pop()
            self.result_box.delete(tk.END)
            self.var_roll.set('?')
        
Drawer()
