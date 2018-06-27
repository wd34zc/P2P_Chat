#获取本机电脑名
import socket

myname = socket.getfqdn(socket.gethostname(  ))
#获取本机ip
myaddr = socket.gethostbyname(myname)
print(myaddr)