import socket

import settings

ip_port = ['127.0.0.1', 9000]  # 电话卡
BUFSIZE = 1024  # 收发消息的尺寸
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 买手机
s.bind(ip_port)  # 手机插卡
s.listen(9100)  # 手机待机

conn, addr = s.accept()  # 手机接电话
# print(conn)
# print(addr)
print('接到来自%s的电话' % addr[0])

msg = conn.recv(BUFSIZE)  # 听消息,听话
print(msg, type(msg))

conn.send(msg.upper())  # 发消息,说话

conn.close()  # 挂电话

s.close()  # 手机关机
