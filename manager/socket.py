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
    ping_ip_num = None
    sever_socket = None
    ip_list = None
    client_socket_dict = {}
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
            SocketManager.ip_list.put(ip_str)
        else:
            if ip_str in SocketManager.ip_alive_list:
                SocketManager.ip_alive_list.remove(ip_str)
                SocketManager.client_socket_dict.pop(ip_str)
        SocketManager.ping_ip_num += 1
        if SocketManager.ping_ip_num == 254:
            print('扫描完毕。')
        else:
            print(SocketManager.ping_ip_num)
            pass

    @staticmethod
    def find_alive_ip(ip=None):
        SocketManager.ping_ip_num = 0
        SocketManager.ip_list = queue.Queue()
        if ip is None:
            ip = SocketManager.sever_ip
        ip_prefix = SocketManager.analyse_ip(ip)
        print("开始扫描ip地址")
        # for i in range(1, 256):
        #     ip = '%s.%s' % (ip_prefix, i)
        #     ThreadManager.get_thread(SocketManager.ping_ip, args=(ip,)).start()
        #     sleep(0.04)

        ip = '10.30.10.229'
        ThreadManager.get_thread(SocketManager.ping_ip, args=(ip,)).start()

    @staticmethod
    def find_alive_client():
        def set_client():
            ip = SocketManager.ip_list.get()
            if ClientSocket.is_exist(ip) is True:
                print(ip)
                SocketManager.client_socket_dict[ip] = None
                SocketManager.ip_alive_list.append(ip)
            else:
                if ip in SocketManager.ip_alive_list:
                    SocketManager.ip_alive_list.remove(ip)
                    SocketManager.client_socket_dict.pop(ip)
        while SocketManager.ping_ip_num < 254:
            while SocketManager.ip_list.empty() is False:
                ThreadManager.get_thread(set_client, args=()).start()
        if SocketManager.ip_list.empty():
            dict = SocketManager.client_socket_dict
            l = SocketManager.ip_alive_list
            # 清理空间
            del SocketManager.ip_list
            gc.collect()

    @staticmethod
    def analyse_ip(ip):
        ip_prefix = re.match('\d{1,3}\.\d{1,3}\.\d{1,3}', ip).group()
        return ip_prefix

    @staticmethod
    def get_my_ip():
        return socket.gethostbyname(socket.gethostname())

    @staticmethod
    def get_server_socket():
        if SocketManager.sever_socket is None:
            SocketManager.sever_socket = SeverSocket()
        return SocketManager.sever_socket

    @staticmethod
    def get_client_socket(host):
        client_socket = ClientSocket(host)
        SocketManager.client_socket_dict[host] = client_socket
        return client_socket

    @staticmethod
    def is_ip_alive(ip):
        flag = ClientSocket.is_exist(ip)
        if flag is False:
            if ip is SocketManager.ip_alive_list:
                SocketManager.ip_alive_list.remove(ip)
        else:
            if ip not in SocketManager.ip_alive_list:
                SocketManager.ip_alive_list.append(ip)
        return flag

    @staticmethod
    def close_socket(ip):
        s = SocketManager.client_socket_dict.get(ip)
        if s is not None:
            s.req_close()

# begin = datetime.today()
# SocketManager.find_alive_ip("10.21.20.1")
# # while SocketManager.ping_ip_num < 254:
# #     sleep(1)
# # print(SocketManager.ip_list)
# # SocketManager.ping_ip("10.21.20.1")
# print(datetime.today() - begin)
