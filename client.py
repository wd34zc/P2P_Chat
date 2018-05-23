import json
import socket

from protocol import SendProtocol, ReceiveProtocol
from settings import SEVER_MSG_PORT


class ClientSocket:

    def __init__(self, host):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = SEVER_MSG_PORT

    def __formatting_msg(self, date_type, msg):
        formate_msg = {
            SendProtocol.CONTENT: msg,
            SendProtocol.TYPE: date_type
        }
        json_msg = json.dumps(formate_msg).encode()
        return json_msg

    def __parse_receive(self, receive_msg):
        receive_msg = json.loads(receive_msg)
        print(receive_msg)
        status = receive_msg[ReceiveProtocol.STATUS]
        if status == ReceiveProtocol.STATUS_SUCCESS:
            print("发送成功")
        else:
            print("发送失败")
            print(ReceiveProtocol.CONTENT)


    def send_msg(self, msg):
        data_type = SendProtocol.TYPE_TEXT
        content = msg
        send_msg = self.__formatting_msg(data_type, content)
        # 连接发送
        s = self.client_socket
        s.connect((self.host, self.port))
        s.send(send_msg)
        # 接收信息
        receive = s.recv(1024)
        self.__parse_receive(receive)


c1 = ClientSocket("192.168.199.184")
c1.send_msg("测试测试")
# c1.send_msg("c222222222222222")
