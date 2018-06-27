# 发送协议
class ClientProtocol:
    TYPE = 'type'
    CONTENT = 'content'
    CODING = 'coding'
    TYPE_EXIST = '001'  # 检测是否能够连通
    TYPE_ALIVE = '001'  # 检测是否连接中
    TYPE_CLOSE = '002'  # 请求断开连接
    TYPE_TEXT = '003'  # 发送文字信息
    TYPE_TEST = '004'  # 用于测试
    TYPE_DEAD = '005'  # 关闭程序


# 回复协议
class ServerProtocol:
    STATUS = 'status' # 状态头
    CONTENT = 'content'

    STATUS_SUCCESS = '01'
    STATUS_ERROR = '02'
    STATUS_OK = '03'
    STATUS_TEST = '04'

