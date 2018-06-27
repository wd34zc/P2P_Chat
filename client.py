import json
import socket
import traceback

from datetime import datetime

from protocol import ServerProtocol, ClientProtocol
from settings import SEVER_MSG_PORT


class ClientSocket:

    def __init__(self, host):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = SEVER_MSG_PORT
        self.is_connect = False
        self.is_close = False
        self.uppdate_timestamp()

    # 转化为json
    def __formatting_msg(self, date_type, msg=''):
        formate_msg = {
            ClientProtocol.CONTENT: msg,
        }
        formate_msg = str(date_type) + json.dumps(formate_msg)
        json_msg = bytes(formate_msg, 'utf8')
        return json_msg

    # 解析返回报文
    def __parse_receive(self, receive_msg):
        # receive_msg = json.loads(receive_msg)
        print(receive_msg)
        status = receive_msg[0:2]
        aa = ServerProtocol.STATUS_SUCCESS
        if status == ServerProtocol.STATUS_SUCCESS:
            print("发送成功")
            return True
        else:
            print("发送失败")
            print(ServerProtocol.CONTENT)
            return False

    def uppdate_timestamp(self):
        self.timestamp = datetime.today()

    def __is_client_exist(self):
        flag = False
        dtype = ClientProtocol.TYPE_EXIST
        if self.is_close is True:
            s = ClientSocket(self.host)
            return s.is_exist()
        try:
            self.connect()
            recv = self.send_status(dtype)
            if recv[0:2] == ServerProtocol.STATUS_OK:
                self.client_socket.close()
                self.is_close = True
                flag = True
            else:
                raise ConnectionRefusedError('连接测试协议异常！')
        except ConnectionRefusedError as e:
            if int(e.errno) == 10061:
                flag = False
            else:
                traceback.print_exc()
        finally:
            return flag

    @staticmethod
    def is_exist(host):
        s = ClientSocket(host)
        return s.__is_client_exist()

    def is_alive(self):
        flag = False
        dtype = ClientProtocol.TYPE_ALIVE
        if self.is_close is True:
            return False
        elif self.is_connect is False:
            self.connect()
        try:
            recv = self.send_status(dtype)
            if recv[0:2] == ServerProtocol.STATUS_OK:
                flag = True
        except ConnectionRefusedError as e:
            if int(e.errno) == 10061:
                flag = False
            else:
                traceback.print_exc()
        finally:
            return flag

    def send_msg(self, msg):
        dtype = ClientProtocol.TYPE_TEXT  # 发送文本类型
        content = msg  # 文本信息
        send_msg = self.__formatting_msg(dtype, content)
        try:
            recv = self.send(send_msg)
        except OSError as e:
            if int(e.errno) == 10056:
                # recv = self.send_without_connect(send_msg)
            # else:
                raise OSError
        return self.__parse_receive(recv)

    def connect(self):
        self.client_socket.connect((self.host, self.port))
        self.is_connect = True

    def send_status(self, dtype, msg=''):
        send_msg = self.__formatting_msg(dtype, msg)
        return self.send(send_msg)

    def send(self, msg):
        # 连接发送
        s = self.client_socket
        s.send(msg)
        # 接收信息
        receive = s.recv(1024)
        # s.close()
        return str(receive, 'utf8')

    def req_close(self):
        if self.is_connect is not True:
            print('该socket还没有连接')
        elif self.is_close is True:
            print('该socket已关闭')
        else:
            dtype = ClientProtocol.TYPE_CLOSE
            send_msg = self.__formatting_msg(dtype)
            recv = self.send(msg=send_msg)
            if recv[0:3] == '003':
                self.client_socket.close()
                self.is_close = True

    def send_without_connect(self, msg):
        s = self.client_socket
        s.send(msg)
        # 接收信息
        receive = s.recv(1024)
        return receive


# c1 = ClientSocket("192.168.199.241")
# c1.connect()
# while True:
#     c1.send(bytes(input(), 'utf8'))