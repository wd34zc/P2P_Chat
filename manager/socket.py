import gc
import os
import platform
import queue
import re
import socket
from time import sleep

from client import ClientSocket
from manager.thread import ThreadManager
from sever import SeverSocket


class SocketManager:
    # settings
    timeout = 1.5
    data_count = 2

    # parameter
    sever_ip = ""
    ping_ip_num = 0
    sever_socket = None
    ip_list = queue.Queue()
    # ip_list = []
    client_socket_list = []
    ip_alive_list = []

    @staticmethod
    def init():
        SocketManager.sever_ip = SocketManager.get_my_ip()

    @staticmethod
    def get_os():
        '''''
        get os 类型
        '''
        os = platform.system()
        if os == "Windows":
            return "n"
        else:
            return "c"

    @staticmethod
    def ping_ip(ip_str):
        timeout = SocketManager.timeout
        data_count = SocketManager.data_count
        string = ip_str + " -w " + str(timeout) + " -n " + str(data_count)
        cmd = ["ping", "-{op}".format(op=SocketManager.get_os()),
               "1", string]
        output = os.popen(" ".join(cmd)).readlines()

        flag = False
        for line in list(output):
            if not line:
                continue
            if str(line).upper().find("TTL") >= 0:
                flag = True
                break
        if flag:
            # print("ip: %s is ok ***" % ip_str)
            SocketManager.ip_list.put(ip_str)
        SocketManager.ping_ip_num += 1
        # print(ip_str)

    @staticmethod
    def find_alive_ip(ip=None):
        if ip is None:
            ip = SocketManager.sever_ip
        thread_list = []
        ip_prefix = SocketManager.analyse_ip(ip)
        print("开始扫描ip地址")
        for i in range(1, 256):
            ip = '%s.%s' % (ip_prefix, i)
            # _thread.start_new_thread(ping_ip, (ip,))
            thread = ThreadManager.get_thread(SocketManager.ping_ip, args=(ip,))
            thread.setDaemon(True)
            thread.start()
            thread_list.append(thread)
            # length = len(thread_list)
            # print(length)
            print(i)
            # if SocketManager.ping_ip_num % 10 == 0:
            sleep(0.04)
        gc.collect()

    @staticmethod
    def find_alive_client():
        def set_client():
            ip = SocketManager.ip_list.get()
            client = SocketManager.get_client_socket(ip)
            if client.is_alive() is True:
                print(ip)
                SocketManager.client_socket_list.append(client)
                SocketManager.ip_alive_list.append(ip)
        while SocketManager.ping_ip_num < 255:
            # if len(SocketManager.ip_list) > 0:
            if SocketManager.ip_list.empty() is False:
                ThreadManager.get_thread(set_client, args=()).start()

    @staticmethod
    def analyse_ip(ip):
        ip_prefix = re.match('\d{1,3}\.\d{1,3}\.\d{1,3}', ip).group()
        return ip_prefix

    @staticmethod
    def get_my_ip():
        return socket.gethostbyname(socket.gethostname())

    @staticmethod
    def get_sever_socket():
        if SocketManager.sever_socket is None:
            SocketManager.sever_socket = SeverSocket()
        return SocketManager.sever_socket

    @staticmethod
    def get_client_socket(host):
        client_socket = ClientSocket(host)
        SocketManager.client_socket_list.append(client_socket)
        return client_socket

# begin = datetime.today()
# SocketManager.find_alive_ip("10.21.20.1")
# # while SocketManager.ping_ip_num < 254:
# #     sleep(1)
# # print(SocketManager.ip_list)
# # SocketManager.ping_ip("10.21.20.1")
# print(datetime.today() - begin)
