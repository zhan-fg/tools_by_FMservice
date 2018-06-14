import os
import re
import shutil
import socket

class Services_test:

    def __init__(self):
        port = self.Task_test()
        PATH_path = self.Path_test()
        service_path = self.Service_test()

        if len(port)==0 and len(PATH_path) == 0 and service_path is None:

            print('请确认是否安装视频会议服务！！！！')

        elif len(port) > 0 and len(PATH_path) > 0 and service_path is not None:

            self.get_log(service_path)
            self.check_port(port)

        elif service_path is not None and len(port) > 0 and len(PATH_path) == 0:

            print('视频会议服务器环境变量异常！！！！')
            self.get_log(service_path)
            self.check_port(port)

        elif service_path is not None and len(port) == 0 and len(PATH_path) > 0:

            print('视频会议服务器未启动,尝试手动启动！')
            self.get_log(service_path)
            if service_path in PATH_path:
                print('视频会议服务器环境变量正常')
            else:
                print('视频会议服务器环境变量异常！！！！')

        elif service_path is None and len(port) > 0 and len(PATH_path) > 0:

            print('视频会议服务异常，是否有杀毒软件或病毒禁用了FMMonitor.exe！！！！')
            for i in PATH_path:
                _path = i[0:i.find('\mysql\bin')]
                self.get_log(_path)
            self.check_port(port)

        elif service_path is None and len(port) == 0 and len(PATH_path) > 0:

            path = self.file_test(PATH_path)
            self.get_log(path)

        elif service_path is not None and len(port) == 0 and len(PATH_path) == 0:

            print('视频会议服务器未启动,尝试手动启动！')

            print('视频会议服务器环境变量异常！！！！')

            self.get_log(service_path)



    def Task_test(self):
        x = ['FM_Server.exe', 'javawebserver.exe', 'mysqlserver.exe', 'FMmonitor.exe']
        port = []
        for i in x:
            try:
                a = os.popen('tasklist /FI "IMAGENAME eq "' + i).readlines()[3]
                print('检测到服务:')
                print(a)
                try:
                    c = re.search(r'\b(\d{3,5})\b', a).group()
                    print('检测PID:' + c + '对应的端口...')
                    b = os.popen('netstat -ano|findstr ' + c).readlines()[0]
                    port.append(b[b.find(':')+1:b.find(':')+5])
                    print('服务开启端口:')
                    print(b)
                except:
                    print('没有检测到服务端口')
            except:
                print('没有检测到服务' + i)

            print('================================================================')
        return port
    def Path_test(self):
        # 查询系统环境变量
        print('检测系统环境变量...')
        FM_path = []
        p = os.getenv('PATH')
        Path_list = re.split(r';', p)
        for i in Path_list:
            path = re.search(r'.{1,}FMServer.{1,}', i)
            if path is not None:
                FM_path.append(path.group())
        if len(FM_path) != 0:
            print('找到FMServer的环境变量:')
            # 环境变量可能有多个
            print(FM_path[0:len(FM_path)])

        print('================================================================')
        return FM_path
    def Service_test(self):
        # 服务状态检测
        print('服务状态检测...')
        a = os.system('sc query FMService')
        if a == 0:
            # 找到FMService服务
            print('找到FMService服务,查询服务状态...')
            b = os.popen('sc qc FMService').readlines()
            for i in b:

                if i.find('AUTO_START') != -1:
                    print('服务状态自动启动')
                elif i.find('DEMAND_START') != -1:
                    print('服务状态手动启动,启动状态异常')
                elif i.find('DISABLED') != -1:
                    print('服务状态禁止启动,启动状态异常')

                if i.find('BINARY_PATH_NAME') != -1:

                 # 根据服务获取程序的安装路径
                    File_path = i[i.find(':') + 2:i.find('FMMonitor\FMMonitor.exe')]
                    print('找到程序根目录')
                    return File_path

        else:
            return None
    def get_log(self, File_path):
        p = os.getcwd()
        if os.path.exists(File_path + 'FMServer\log'):
            if os.path.exists(p + '\log\FMServerlog'):
                print('FMServerlog已存在')
            else:
                try:
                    shutil.copytree(File_path + 'FMServer\log', p + '\log\FMServerlog')
                    print('FMServer日志拷贝成功')
                except:
                    print('FMServer日志拷贝失败')
        else:
            print('文件路径：'+File_path + 'FMServer\log 不存在')
        if  os.path.exists(File_path + 'tomcat\webapps\logs'):
            if os.path.exists(p + '\log\weblog'):
                print('weblog已存在')
            else:
                try:
                    shutil.copytree(File_path + 'tomcat\webapps\logs', p + '\log\weblog')
                    print('web日志拷贝成功')
                except:
                    print('web日志拷贝失败')
        else:
            print('文件路径：'+File_path + 'tomcat\webapps\logs 不存在')

    def check_port(self,port):

        failed_port = []
        for _each_port in port:
            # print i
            try:
                sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sk.settimeout(3)
                sk.connect(('localhost', int(_each_port)))
                sk.close
                print(str(_each_port)+'可以创建链接')
                
            except socket.error:
                failed_port.append(_each_port)
                print(str(_each_port) + '创建链接异常')

    def file_test(self,PATH_path):
        for i in PATH_path:
            if os.path.exists(i):
                _path = i[0:i.find('\mysql\bin')]
                if os.path.exists(_path + 'FMServer\FM_Server.exe') and os.path.exists(_path + 'mysql\bin\mysqlserver.exe') and os.path.exists(_path + 'tomcat\start.bat'):
                    print('视频会议服务异常，是否有杀毒软件或病毒禁用了FMMonitor.exe！！！！')
                elif os.path.exists(_path + 'FMServer\FM_Server.exe') is False and os.path.exists(_path + 'mysql\bin\mysqlserver.exe') is False and os.path.exists(_path + 'tomcat\start.bat') is False:
                    print('请确认是否安装视频会议服务！！！！')
                else:
                    print('请确认视频会议服务程序是否文件缺失！！！！')
                return _path
            else:
                print('无效环境变量:'+ i)

s_test = Services_test()
