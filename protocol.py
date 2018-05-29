# 发送协议
class SendProtocol:
    TYPE = 'type'
    CONTENT = 'content'
    CODING = 'coding'
    TYPE_TEXT = 'text'  # 发送文字信息
    TYPE_ALIVE = 'alive'  # 检测是否能够连通


# 回复协议
class ReceiveProtocol:
    STATUS = 'status'
    CONTENT = 'content'

    STATUS_SUCCESS = 'success'
    STATUS_ERROR = 'error'
