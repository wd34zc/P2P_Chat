import socket

ip_port = ('127.0.0.1', 9000)
BUFSIZE = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect_ex(ip_port)  # 拨电话

s.send('nitouxiang nb'.encode('utf-8'))  # 发消息,说话(只能发送字节类型)

feedback = s.recv(BUFSIZE)  # 收消息,听话
print(feedback.decode('utf-8'))

s.close()  # 挂电话
