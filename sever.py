import json
import re
import socket
import traceback

import chat_service
from manager.thread import ThreadManager
from protocol import ServerProtocol, ClientProtocol
from settings import SEVER_MSG_PORT


class SeverSocket:
    def __init__(self):
        host = self.get_sever_host()
        port = SEVER_MSG_PORT
        ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ss.bind((host, port))
        ss.listen(20)
        self.host = host
        self.port = port
        self.server_socket = ss
        print("服务器地址：" + socket.gethostbyname(host))
        print("监听端口：" + str(port))

    def get_sever_host(self):
        addrs = socket.getaddrinfo(socket.gethostname(), None)
        sever_ip = None
        for addr in addrs:
            ip = addr[4][0]
            if re.match('^\d+.\d+.\d+.\d+$', ip) is not None:
                ids = ip.split('.')
                if ids[0] == '192' and ids[1] == '168':
                    sever_ip = ip
                elif ids[0] == '172' and (ids[1] >= 16 and ids[1] <= 31):
                    sever_ip = ip
                elif ids[0] == '10':
                    sever_ip = ip
            # sever_ip = ip = addrs[-1][4][0]

        # print(sever_ip)
        return sever_ip

    def __formatting_msg(self, status, msg=''):
        formate_msg = {
            ServerProtocol.CONTENT: msg
        }
        json_msg = status + json.dumps(formate_msg)
        return bytes(json_msg, 'utf8')

    def __parse(self, dtype, clint_msg, address):
        msg = {'address': address}
        clint_msg = json.loads(clint_msg)
        if dtype == ClientProtocol.TYPE_TEXT:
            content = clint_msg[ClientProtocol.CONTENT]
            chat_service.update_message(content)
        else:
            pass

    def resp_close(self, conn):
        conn.close()

    def listen(self):
        def init_connection(conn, url):
            while True:
                try:
                    recv = conn.recv(1024)
                    # print(recv)
                    if recv == '' or len(recv) == 0:
                        # print('获取不到消息')
                        continue
                    else:
                        recv = str(recv, 'utf8')
                        status = recv[0:3]
                        if status == ClientProtocol.TYPE_CLOSE:  # 请求关闭
                            break
                        elif status == ClientProtocol.TYPE_EXIST:  # 请求是否在线
                            send_ok(conn)
                            conn.close()
                            break
                        elif status == ClientProtocol.TYPE_ALIVE:
                            send_ok(conn)
                        elif status == ClientProtocol.TYPE_TEXT:  # 接受消息
                            self.__parse(status, recv[3:], url)
                            send_status(conn, ServerProtocol.STATUS_SUCCESS)
                        elif status == ClientProtocol.TYPE_TEST:
                            send_ok(conn)
                        else:
                            print('协议异常!')
                            break
                except Exception as e:
                    traceback.print_exc()
                    status = ServerProtocol.STATUS_ERROR
                    msg = e.args
                    send_msg = self.__formatting_msg(status, msg)
                    conn.send(send_msg)
            conn.close()
            print('连接已关闭:' + url)

        def send_ok(conn):
            send_status(conn, ServerProtocol.STATUS_OK)

        def send_status(conn, status):
            conn.send(self.__formatting_msg(status))

        while True:
            # 建立客户端连接
            conn, address = self.server_socket.accept()
            print('获取到链接：' + address[0])
            ThreadManager.get_thread(init_connection, args=(conn, address[0],)).start()

# s = SeverSocket()
# s.listen()
# # host = socket.gethostname()
# # port = SEVER_MSG_PORT
# # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# # s.bind((host, port))
# # s.listen(20)
# while True:
#     conn, address = s.server_socket.accept()
#     # recv = conn.recv(1024)
#     while True:
#         recv = conn.recv(1024)
#         print(recv)
#         if recv == '':
#             conn.send(bytes('ok + 空字符串', 'utf8'))
#         else:
#             recv = str(recv, 'utf8')
#             conn.send(bytes('ok + %s' % recv, 'utf8'))
#         if recv == 'eeee':
#             break
#     conn.close()
