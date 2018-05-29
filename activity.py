import socket

from datetime import datetime
from time import sleep

from SocketManager import SocketManager

from ThreadManager import ThreadManager

# 生成服务端
sever = SocketManager.get_sever_socket()
sever_thread = ThreadManager.get_thread(sever.listen, args=())
sever_thread.setDaemon(True)
sever_thread.start()

# 客户端
begin = datetime.today()
SocketManager.init()
SocketManager.find_alive_ip("10.21.20.21")
SocketManager.find_alive_client()
t = ThreadManager.get_thread(SocketManager.find_alive_client, args=())
t.start()
t.join()
print(datetime.today() - begin)


# ip_list = SocketManager.find_ip(my_ip)
#
# # ip_list = ['192.168.199.1', '192.168.199.107', '192.168.199.110', '192.168.199.135', '192.168.199.141', '192.168.199.159', '192.168.199.167', '192.168.199.184', '192.168.199.187', '192.168.199.209']
# print(ip_list)
# client_list = []
# thread_list = []
# for ip in ip_list:
#     client = SocketManager.get_client_socket(ip)
#     client_list.append(client)
#     t = ThreadManager.get_thread(client.is_alive, args=())
#     t.start()
#     t.remark = client
#     thread_list.append(t)
# print("生成客户端完毕")
# begin = datetime.today()
# # for t in thread_list:
#     # t.join()
#     # if t.get_result() is False:
#     #     client_list.remove(t.remark)
# for t in ThreadManager.get_finish_thread(thread_list):
#     print(t)
#     if t.get_result() is False:
#         client_list.remove(t.remark)
#         print("删除：", t.remark)
# print("jieshu")
# end = datetime.today()
# print(end-begin)
#
# print(client_list)
