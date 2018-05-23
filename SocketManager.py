import os
import platform

from datetime import datetime

from ThreadManager import ThreadManager


class SocketManager:
    timeout = 2

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
        string = ip_str + " -w " + str(timeout)
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
            return ip_str
        else:
            return None

    @staticmethod
    def find_ip(ip_prefix):
        ip_list = []
        thread_list = []
        print("开始扫描ip地址")
        begin = datetime.today()
        for i in range(1, 256):
            ip = '%s.%s' % (ip_prefix, i)
            # _thread.start_new_thread(ping_ip, (ip,))
            thread = ThreadManager.get_thread(SocketManager.ping_ip, args=(ip,))
            thread.start()
            thread_list.append(thread)
        for t in thread_list:
            t.join()
            result = t.get_result()
            if result is not None:
                ip_list.append(result)
        end = datetime.today()
        consuming = end - begin
        print(consuming)


# ping_ip("10.21.20.0", 1.5)
# find_ip("127.0.0")
# find_ip("192.168.199")
SocketManager.find_ip("10.21.20")
