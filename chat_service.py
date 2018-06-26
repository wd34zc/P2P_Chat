import os
from time import sleep

from manager.socket import SocketManager
from manager.thread import ThreadManager
from recorder import Recorder

on_line_ip = {}


def send_to_remote(message, ip):
    SocketManager.get_my_ip()
    socket = SocketManager.client_socket_dict.get(ip)
    if socket is None:
        if SocketManager.sever_ip == ip:
            socket = SocketManager.get_client_socket(ip)
            socket.connect()
    if socket is not None:
        if socket.send_msg(message) is True:
            Recorder.write_to_recorder(ip, message + '\n\n')
            return True
    return False


def start_server_socket():
    # 生成服务端
    sever = SocketManager.get_server_socket()
    sever_thread = ThreadManager.get_thread(sever.listen, args=())
    sever_thread.setDaemon(True)
    sever_thread.start()
    return SocketManager.get_my_ip()


def get_online_client():
    # 客户端
    SocketManager.init()
    # ip = "10.21.20.21"
    ip = SocketManager.sever_ip
    ThreadManager.get_thread(SocketManager.find_alive_ip, args=(ip,)).start()
    ThreadManager.get_thread(SocketManager.find_alive_client, args=()).start()
    return SocketManager.ip_alive_list


def is_ip_alive(ip):
    return SocketManager.is_ip_alive(ip)


def connect_ip(ip):
    s = SocketManager.get_client_socket(ip)
    s.connect()


def close_ip(ip):
    SocketManager.close_socket(ip)


def update_recorders():
    while True:
        sleep(60)
        ips = SocketManager.ip_alive_list
        recorders = os.listdir('recorders')
        for r in recorders:
            if r not in ips:
                Recorder.delete_recorder(r)


def update_message(content):
    # print(content)
    rip = content.split('\n')[0]
    if rip != SocketManager.sever_ip:
        from gui import chat_windows
        chat_windows.update_message_box(content)
        Recorder.write_to_recorder(rip, content)


ThreadManager.get_thread(update_recorders, args=()).start()
