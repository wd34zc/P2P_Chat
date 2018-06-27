import re
import socket
#获取本机电脑名
myname = socket.getfqdn(socket.gethostname())
#获取本机ip
myaddrs = socket.gethostbyname(myname)
print(myaddrs)

# A类地址：10.0.0.0--10.255.255.255
# B类地址：172.16.0.0--172.31.255.255
# C类地址：192.168.0.0--192.168.255.255
addrs = socket.getaddrinfo(socket.gethostname(), None)
sever_ip = None
for addr in addrs:
    ip = addr[4][0]
    if re.match('^\d+.\d+.\d+.\d+$', ip) is not None:
        ids = ip.split('.')
        if ids[0] == '192' and ids[1] == '168':
            sever_ip = ip
            break
        elif ids[0] == '172' and (ids[1] >=16 and ids[1] <= 31):
            sever_ip = ip
        elif ids[0] == '10':
            sever_ip = ip

print(sever_ip)