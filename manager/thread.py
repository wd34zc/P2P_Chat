import math
import threading
from time import sleep


class ThreadManager(object):
    thread_list = []
    thread_max = 260
    interval = 7  # 单位：秒

    class Thread(threading.Thread):
        def __init__(self, func, args=(), level=3):
            super().__init__()
            self.func = func
            self.args = args
            self.result = None
            self.remark = None
            self.level = level
            self.finish = 0

        def set_func(self, func, args=()):
            self.func = func
            self.args = args

        def set_level(self, level):
            self.level = level

        def start(self):
            super().start()

        def run(self):
            self.result = self.func(*self.args)

        def get_result(self):
            try:
                return self.result  # 如果子线程不使用join方法，此处可能会报没有self.result的错误
            except Exception:
                return None

    @staticmethod
    def init():
        # 启动线程回收线程
        # tc_thread = ThreadManager.get_thread(ThreadManager.__thread_collection, args=(), level=1)
        # print("TC线程：", tc_thread)
        # tc_thread.setDaemon(True)
        # tc_thread.start()
        pass

    @staticmethod
    def get_thread(func, args=(), level=3):
        flag = 1
        max = ThreadManager.thread_max
        tl = ThreadManager.thread_list
        thread = None
        if len(ThreadManager.thread_list) == ThreadManager.thread_max:
            ThreadManager.collect_thread()
        thread = ThreadManager.Thread(func, args, level)
        ThreadManager.thread_list.append(thread)
        return thread

    @staticmethod
    def collect_thread():
        thread = ThreadManager.Thread(ThreadManager.__collect, args=(), level=1)
        ThreadManager.thread_list.append(thread)
        thread.start()
        return thread

    @staticmethod
    def __collect():
        # print("正在回收线程")
        lock = threading.Lock()
        lock.acquire()
        for t in ThreadManager.thread_list:
            if not t.is_alive():
                ThreadManager.thread_list.remove(t)
                # print('回收线程：', t)

        lock.release()
        # print("线程回收结束")

    @staticmethod
    def __thread_collection():
        criticality = math.ceil(ThreadManager.thread_max * 0.9)
        thread = None
        while True:
            if len(ThreadManager.thread_list) > criticality:
                if thread is None:
                    thread = ThreadManager.collect_thread()
                elif thread.is_alive() is True:
                    pass
                else:
                    thread = ThreadManager.collect_thread()
            sleep(ThreadManager.interval)

    @staticmethod
    def show_thread_list():
        for my_thread in ThreadManager.thread_list:
            print(my_thread)

    @staticmethod
    def get_list_amount():
        return len(ThreadManager.thread_list)


    @staticmethod
    def remove_thread(t):
        if t in ThreadManager.thread_list:
            ThreadManager.thread_list.remove(t)

    @staticmethod
    def get_finish_thread(thread_list):
        while len(thread_list):
            for t in thread_list:
                if t.is_alive is False:
                    yield t
                    thread_list.remove(t)
