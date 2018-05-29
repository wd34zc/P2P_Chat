import tkinter as tk
from time import sleep

import service
from manager.thread import ThreadManager

ip_alive_list = []
server_ip = None


def init():
    # 内部函数
    def update():
        while True:
            update_friendBox()
            sleep(60)
    global server_ip
    global ip_alive_list
    server_ip = service.start_server_socket()
    # ip_alive_list = service.get_online_client()
    ThreadManager.get_thread(update, args=(), level=1)


def add_alive_list(ip):
    ip_alive_list.append(ip)


def update_friendBox():
    old = friend_tuple.get()
    new = ip_alive_list
    for ip in new:
        if ip not in old:
            friendsListbox.insert(ip)
    for ip in old:
        if ip not in new:
            friendsListbox.delete(ip)


def send_button():
    messageInput = inputText.get(1.0, tk.END)
    print(messageInput)
    messageText.insert(tk.END, messageInput + '\n\n')
    service.send_to_remote(messageInput)
    inputText.delete(1.0, tk.END)


def select_friend(event):
    print("select_friend")
    print(friendsListbox.get(friendsListbox.curselection()))
    # print(friends.get())

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
l1 = tk.Label(f1, text='在线列表:', bg='white').pack(anchor='w', padx='1', pady='3')
friend_tuple = tk.StringVar()
friend_tuple.set(tuple(ip_alive_list))
friendsListbox = tk.Listbox(f1, listvariable=friend_tuple)
friendsListbox.bind('<Double-Button-1>', select_friend)
friendsListbox.pack(fill='y', expand=1, ipadx='3', ipady='3')

# 消息显示框架 f2
l2 = tk.Label(f2, text='消息窗口:', bg='white').pack(anchor='w', padx='1', pady='3')
messageText = tk.Text(f2)
messageText.pack(fill='y', ipadx='3', ipady='3')

# 输入框架 f3
inputText = tk.Text(f3, width='100', height='6')
inputText.pack(padx='3', pady='3')
send = tk.Button(f3, text='发送', command=send_button, width='8', height='1').pack(side='right')

f1.pack(side='left', fill='y')
f2.pack(side='top', fill='x')
f3.pack(side='bottom', fill='x')

tk.mainloop()
