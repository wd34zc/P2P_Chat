import os
import shutil

directory = 'recorders/'

class Recorder:
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
        Recorder.manager[ip] = 1

    @staticmethod
    def delete_recorder(ip):
        if Recorder.manager.get(ip) is not None:
            Recorder.manager.pop(ip)
        path = directory + ip
        if os.path.exists(path):
            os.remove(path)

    @staticmethod
    def have_read(ip):
        if Recorder.manager.get(ip) is not None:
            Recorder.manager[ip] = 0

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