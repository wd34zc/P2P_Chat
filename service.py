import datetime

from manager.socket import SocketManager
from manager.thread import ThreadManager


def send_to_remote(message, ip):
    pass

def start_server_socket():
    # 生成服务端
    sever = SocketManager.get_sever_socket()
    sever_thread = ThreadManager.get_thread(sever.listen, args=())
    sever_thread.setDaemon(True)
    sever_thread.start()
    return SocketManager.get_my_ip()

def get_online_client():
    # 客户端
    SocketManager.init()
    SocketManager.find_alive_ip("10.21.20.21")
    SocketManager.find_alive_client()
    t = ThreadManager.get_thread(SocketManager.find_alive_client, args=())
    t.start()
    t.join()
    return SocketManager.ip_alive_list
