import os
import shutil

directory = 'recorders/'


class RecorderManager:
    manager = {}
    if os.path.exists('recorders'):
        shutil.rmtree('recorders')
    os.mkdir('recorders')

    @staticmethod
    def write_to_recorder(ip, content):
        file = directory + ip
        f = open(file, 'a+')
        f.write(content)
        f.close()
        RecorderManager.manager[ip] = True

    @staticmethod
    def delete_recorder(ip):
        if RecorderManager.manager.get(ip) is not None:
            RecorderManager.manager.pop(ip)
        path = directory + ip
        if os.path.exists(path):
            os.remove(path)

    @staticmethod
    def have_read(ip):
        if RecorderManager.manager.get(ip) is not None:
            RecorderManager.manager[ip] = False

    @staticmethod
    def get_recorder(ip):
        name = directory + '' + ip
        if os.path.exists(name):
            f = open(name, 'r')
            a = f.read()
            f.close()
        else:
            a = ''
        return a
