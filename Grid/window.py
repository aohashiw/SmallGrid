import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

import time
from tkinter import *
import numpy as np
from Grid.Test import update_value
from Grid.Test import update_policy

root = Tk() # 初始化Tk()
root.title("SmallGrid")    # 设置窗口标题
root.geometry("800x600")    # 设置窗口大小 注意：是x 不是*
mygrid = Frame(root)
cv = Canvas(mygrid,bg = 'white',width=440,height=440)
cv_v = Canvas(mygrid,width=440,height=440)

Label(root,text='设置长度：').place(x=270,y=0)
Label(root,text='设置宽度：').place(x=270,y=20)
Label(root,text='点击重置更新长宽').place(x=370,y=70)
var1 = StringVar()
e1 = Entry(root, textvariable = var1)
var1.set("4")
e1.pack()

var = StringVar()
e2 = Entry(root, textvariable = var)
var.set("3")
e2.pack()

high = e1.get()
wide = e2.get()

high = int(high)
wide = int(wide)

VALUE = np.zeros([wide,high])
RANDOM_POLICY = np.linspace(0.25, 0.25, num=4*wide*high,dtype=np.float).reshape([wide,high,4])
POLICY = RANDOM_POLICY
values = []
lines = []

#   Initial
rectangle = [([0] * 10) for i in range(10)]
def initial(wide,high):
    global rectangle
    for i in range(0,wide):
        for j in range(0, high):

            rectangle[i][j] = cv.create_rectangle(10 + i * 80, 10 + j * 80, 90 + i * 80, 90 + j * 80)

    for i in range(0,wide):
        for j in range(0, high):
            value = ("%.2f" % VALUE[i][j])
            values.append(cv.create_text(30 + i * 80, 20 + j * 80, text = value,tag = ('value')))
initial(wide,high)

def show_value(wide,high):
    for i in range(0, wide):
        for j in range(0, high):
            index = i * high + j
            cv.delete(values[index])
            value = ("%.2f" % VALUE[i][j])
            values[index] = (cv.create_text(30 + i * 80, 20 + j * 80, text=value))
    root.update()

def show_policy():
    for line in lines:
        cv.delete(line)
    for i in range(wide):
        for j in range(high):
            if (i == 0 and j == 0) or (i == wide-1 and j == high-1):
                continue
            if POLICY[i][j][0] !=0:
                lines.append(cv.create_line(50 + i * 80, 20 + j * 80, 50 + i * 80, 50 + j * 80,arrow="first"))
            if POLICY[i][j][1] !=0:
                lines.append(cv.create_line(50 + i * 80, 50 + j * 80, 50 + i * 80, 80 + j * 80, arrow="last"))
            if POLICY[i][j][2] !=0:
                lines.append(cv.create_line(20 + i * 80, 50 + j * 80, 50 + i * 80, 50 + j * 80,arrow="first"))
            if POLICY[i][j][3] !=0:
                lines.append(cv.create_line(50 + i * 80, 50 + j * 80, 80 + i * 80, 50 + j * 80,arrow="last"))
    root.update()




def single_update():
    global VALUE,POLICY,wide,high
    VALUE = update_value(VALUE,POLICY,wide,high)
    show_value(wide,high)

def continue_update():
    global VALUE,POLICY,wide,high
    MY_POLICY = POLICY
    new_VALUE = update_value(VALUE,MY_POLICY,wide,high)
    while not((VALUE == new_VALUE).all()):
        VALUE = new_VALUE
        show_value(wide,high)
        new_VALUE = update_value(VALUE,MY_POLICY,wide,high)

def policy_update():
    global POLICY,wide,high
    POLICY = update_policy(VALUE,wide,high)
    show_policy()

def cross_update():
    global VALUE,POLICY,wide,high
    show_policy()
    new_VALUE = update_value(VALUE, POLICY,wide,high)
    while not ((VALUE == new_VALUE).all()):
        time.sleep(0.5)
        VALUE = new_VALUE
        POLICY = update_policy(VALUE,wide,high)
        show_value(wide,high)
        show_policy()
        new_VALUE = update_value(VALUE, POLICY,wide,high)

def delate():#删除原来的rectangular，text
    for i in range(0, wide):
        for j in range(0, high):
            cv.delete(rectangle[i][j])
            index = i * high + j
            cv.delete(values[index])
        for line in lines:
            cv.delete(line)

def reset():
    global VALUE,POLICY,wide,high,rectangle,values
    delate()
    high = e1.get()
    wide = e2.get()
    high = int(high)
    wide = int(wide)
    RANDOM_POLICY = np.linspace(0.25, 0.25, num=4 * wide * high, dtype=np.float).reshape([wide, high, 4])
    POLICY = RANDOM_POLICY
    VALUE = np.zeros([wide, high])
    values = []
    initial(wide, high)
    show_value(wide,high)
    root.update()
    show_policy()

btns= Frame(root)
singlebtn= Button(btns, text="单步值迭代", command=single_update).pack(side=LEFT)
continuebtn = Button(btns, text="连续值迭代", command=continue_update).pack(side=LEFT)
updatepibtn= Button(btns, text="策略更新", command=policy_update).pack(side=LEFT)
crossbtn= Button(btns, text="交叉更新", command=cross_update).pack(side=LEFT)
reset_btn= Button(btns, text="重置", command=reset).pack(side=LEFT)

btns.place(relx=0.32,rely=0.2)
cv.pack()
mygrid.place(relx=0.3,rely=0.3)

root.mainloop()