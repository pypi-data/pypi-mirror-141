"""
日志相关文件操作类
"""
import os
from sys import _getframe as get_run_info
import platform
import datetime

try:
    import xml.etree.cElementTree as XMLTree
except ImportError:
    import xml.etree.ElementTree as XMLTree


def create_log_file(file_name):
    """
    创建日志文件
    :param file_name: 文件名称
    :return: None
    """
    # 判断日志路径是否存在
    if not os.path.exists(os.path.dirname(file_name)):
        try:
            os.makedirs(os.path.dirname(file_name))
        except FileExistsError as e:
            print(str(e))

    # 判断日志文件是否存在
    if not os.path.exists(file_name):
        try:
            os.mknod(file_name)
        except AttributeError as e:
            print(str(e))
            f = open(file_name, 'w')
            f.close()


class FileOption:

    def __init__(self, conf_path, conf_deep):
        """
        类初始化
        :param conf_path: 配置文件路径
        :param conf_deep: 配置文件搜索深度
        """
        # 设置配置文件路径
        if conf_path == '':
            self.conf_path = os.getcwd() + '/eqlog.xml'
        elif conf_path[-4:] == '.xml':
            self.conf_path = conf_path
        elif conf_path[-1:] == '/' or conf_path[-1:] == '\\':
            self.conf_path = conf_path + 'eqlog.xml'
        else:
            self.conf_path = conf_path + '/eqlog.xml'
        # 配置文件读取深度
        self.conf_deep = conf_deep
        # 日志文件记录目录
        self.logfile_path = ''
        # 当前系统运行环境
        self.env = 'win_path' if platform.system().lower() == 'windows' else 'linux_path'
        # 控制台输出标志
        self.console = False

    def config_path_read(self, deep=1):
        """
        配置文件存在性校验
        :param deep: 搜索深度
        :return: None
        """
        if not os.path.exists(self.conf_path):
            eqlog_dir = os.path.dirname(self.conf_path) + '/eqconfig/eqlog.xml'
            if not os.path.exists(eqlog_dir) and deep <= self.conf_deep:
                self.conf_path = os.path.abspath(os.path.join(os.path.dirname(self.conf_path), "..")) + '/eqlog.xml'
                self.config_path_read(deep + 1)
            else:
                self.conf_path = eqlog_dir

    def read_xml(self, conf_path=''):
        """
        读取xml文件配置
        :param conf_path: 配置文件路径
        :return: None
        """
        conf_path = self.conf_path if conf_path == '' else conf_path
        now = datetime.datetime.now()
        try:  # 读取日志文件所在目录
            xml_tree = XMLTree.parse(conf_path)
            xml_root = xml_tree.getroot()
            self.logfile_path = xml_root.find('file_path').find(self.env).text
        except Exception as e:
            print(now.strftime("%Y-%m-%d %H:%M:%S"), '[WARNING]', '[eqlog]',
                  f"[{__file__}, {get_run_info().f_code.co_name}(), line {get_run_info().f_lineno}]",
                  '[Get log file path]', str(e))
        try:  # 读取控制台输出标志
            xml_tree = XMLTree.parse(conf_path)
            xml_root = xml_tree.getroot()
            self.console = True if xml_root.find('console').text == 'true' else False
        except Exception as e:
            print(now.strftime("%Y-%m-%d %H:%M:%S"), '[WARNING]', '[eqlog]',
                  f"[{__file__}, {get_run_info().f_code.co_name}(), line {get_run_info().f_lineno}]",
                  '[Get console output config]', str(e))
