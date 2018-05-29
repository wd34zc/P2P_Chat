import tkinter as tk

import service


def send_button(message):
    messageInput = inputText.get(1.0, tk.END)
    print(messageInput)
    messageText.insert(tk.END, messageInput + '\n\n')
    service.send_to_remote(messageInput)
    inputText.delete(1.0, tk.END)


root = tk.Tk()
root.title("test")
root.geometry('720x480')
root.resizable(width=False, height=False)

f1 = tk.Frame(width='130', height='400', bg='red')
f2 = tk.Frame(width='130', height='350', bg='blue')
f3 = tk.Frame(width='130', height='150', bg='yellow')
f4 = tk.Frame(width='130', height='150', bg='green')

# 好友列表 f1
l1 = tk.Label(f1, text='在线列表:', bg='white').pack(anchor='w', padx='1', pady='3')
var = tk.StringVar()
lb = tk.Listbox(f1, listvariable=var)
lb.pack(fill='y', expand=1, ipadx='3', ipady='3')

# 消息显示框架 f2
l2 = tk.Label(f2, text='消息窗口', bg='white').pack(anchor='w', padx='1', pady='3')
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
