import re
import tkinter as tk

from datetime import datetime
from time import sleep
from tkinter import messagebox

import chat_service
from manager.thread import ThreadManager

server_ip = ''
talking_ip = ''


def init():
    # 内部函数
    def update():
        while True:
            update_friendBox()
            sleep(20)

    def get_news():
        while True:
            if server_ip != talking_ip:
                if chat_service.have_new_message(talking_ip):
                    messageText.config(state=tk.NORMAL)
                    messageText.delete(1.0, tk.END)
                    messages = chat_service.get_recorder(talking_ip)
                    messageText.insert(tk.END, messages)
                    messageText.mark_set('test_mark', tk.CURRENT + ' wordend')
                    messageText.config(state=tk.DISABLED)
            sleep(5)


    global server_ip
    global ip_alive_list
    global talking_ip
    server_ip = chat_service.start_server_socket()
    ip_alive_list = chat_service.get_online_client()
    talking_ip = server_ip
    chat_service.connect_ip(server_ip)
    ThreadManager.get_thread(update, args=(), level=1).start()
    ThreadManager.get_thread(get_news, args=(), level=1).start()


def add_alive_list(ip):
    ip_alive_list.append(ip)


def update_friendBox():
    if 'friend_tuple' in globals().keys():
        print('更新。。。')
        l = []
        str = friend_tuple.get()
        l = re.findall("\\'([\w\d.]+)\\'", str)
        new = chat_service.get_ip_alive_list()
        for ip in new:
            if ip not in l:
                l.append(ip)
        for ip in l:
            if ip not in new:
                l.remove(ip)
        friend_tuple.set(tuple(l))


# 发送消息
def send_button():
    def format_message(message):
        dtime = datetime.strftime(datetime.today(), '%y-%m-%d %H:%M:%S')
        fm = '%s\n%s%s' % (server_ip, message, dtime)
        return fm
    # 格式化
    msg = inputText.get(1.0, tk.END)
    if len(msg.strip()) <= 1:
        messagebox.showinfo("提示", '消息不能为空')
        return
    msg = format_message(msg)
    print(msg)
    # 发送
    flag = chat_service.send_to_remote(msg, talking_ip)
    messageText.config(state=tk.NORMAL)
    if flag:
        messageText.insert(tk.END, msg + '\n')
    else:
        messageText.insert(tk.END, msg + '\n（发送失败）\n')
    messageText.config(state=tk.DISABLED)
    inputText.delete(1.0, tk.END)


# 监听窗口
def update_message_box(message):
    # print(message)
    messageText.insert(tk.END, message + '\n\n')
    # print('aaaaaaaaaa')


# 选择朋友
def select_friend(event):
    selection = friendsListbox.curselection()
    if len(selection) > 0:
        ip = friendsListbox.get(selection)
        if ip != server_ip:
            if chat_service.is_ip_alive(ip):
                global talking_ip
                # 先关闭就链接
                chat_service.close_ip(talking_ip)
                # 开启新链接
                chat_service.connect_ip(ip)
                talking_ip = ip
                l2_var.set(get_lable2_text())
                # 重新获取记录
                messageText.delete(1.0, tk.END)
                messages = chat_service.get_recorder(ip)
                messageText.insert(tk.END, messages)
            else:
                messagebox.showinfo("提示", '该用户已下线')


# 获取聊天窗口标题文本
def get_lable2_text():
    text = '与%s聊天中...' % talking_ip
    if talking_ip == server_ip:
        text += '(自己)'
    return text



init()
root = tk.Tk()
root.title("P2P_Chat(%s)" % str(server_ip))
root.geometry('720x480')
root.resizable(width=False, height=False)

f1 = tk.Frame(width='130', height='400', bg='red')
f2 = tk.Frame(width='130', height='350', bg='blue')
f3 = tk.Frame(width='130', height='150', bg='yellow')
f4 = tk.Frame(width='130', height='150', bg='green')

# 好友列表 f1
l1 = tk.Label(f1, text='在线列表:', bg='red').pack(anchor='w', padx='1', pady='3')
friend_tuple = tk.StringVar()
# friend_tuple.set(tuple(ip_alive_list))
# friend_tuple.set(('aa', 'bb', 'cc'))
friendsListbox = tk.Listbox(f1, listvariable=friend_tuple)
friendsListbox.bind('<Double-Button-1>', select_friend)
friendsListbox.pack(fill='y', expand=1, ipadx='3', ipady='3')

# 消息显示框架 f2
l2_var = tk.StringVar()
l2_var.set(get_lable2_text())
l2 = tk.Label(f2, textvariable=l2_var, bg='white')
l2.pack(anchor='w', padx='1', pady='3')

messageText = tk.Text(f2)
messageText.config(state=tk.DISABLED)
messageText.pack(fill='y', ipadx='3', ipady='3')

# 输入框架 f3
inputText = tk.Text(f3, width='100', height='6')
inputText.pack(padx='3', pady='3')
send = tk.Button(f3, text='发送', command=send_button, width='8', height='1').pack(side='right')

f1.pack(side='left', fill='y')
f2.pack(side='top', fill='x')
f3.pack(side='bottom', fill='x')

tk.mainloop()
