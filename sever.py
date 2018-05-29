import json
import socket
import traceback

from protocol import ReceiveProtocol, SendProtocol
from settings import SEVER_MSG_PORT


class SeverSocket:
    def __init__(self):
        host = socket.gethostname()
        port = SEVER_MSG_PORT
        ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ss.bind((host, port))
        ss.listen(20)
        self.server_socket = ss
        print("服务器地址：" + socket.gethostbyname(host))
        print("监听端口：" + str(port))

    def get_sever_host(self):
        s = self.server_socket
        pass

    def __formatting_msg(self, status, msg):
        formate_msg = {
            ReceiveProtocol.STATUS: status,
            ReceiveProtocol.CONTENT: msg
        }
        json_msg = json.dumps(formate_msg).encode()
        return json_msg

    def __parse(self, clint_msg, address):
        msg = {'address': address}
        clint_msg = json.loads(clint_msg)
        data_type = clint_msg[SendProtocol.TYPE]
        if data_type == SendProtocol.TYPE_TEXT:
            content = clint_msg[SendProtocol.CONTENT]
            msg['content'] = content
            print(msg)
        if data_type == SendProtocol.TYPE_ALIVE:
            pass

    def listen(self):
        while True:
            # 建立客户端连接
            try:
                client_socket, address = self.server_socket.accept()
                receive_msg = client_socket.recv(1024)
                self.__parse(receive_msg, address)
                send_msg = self.__formatting_msg(ReceiveProtocol.STATUS_SUCCESS, "接收成功")
            except Exception as e:
                traceback.print_exc()
                status = ReceiveProtocol.STATUS_ERROR
                msg = e
                send_msg = self.__formatting_msg(status, msg)
            client_socket.send(send_msg)
            client_socket.close()


# socket = SeverSocket()
# socket.listen()
