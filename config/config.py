import os

from fishbase import conf_as_dict, set_log_file, logger
from fishbase.fish_object import SingleTon

basedir = os.path.split(os.path.dirname(__file__))[0]
conf_folder_path = os.path.join(basedir, 'config')
project_name = os.path.split(basedir)[-1]


class EyesConfig(SingleTon):

    def __init__(self):
        self.dt = {}
        self.get_config_info()

    def get_config_info(self):
        config_path = os.path.join(conf_folder_path, 'config.conf')
        conf_info_tuple = conf_as_dict(config_path)
        self.dt = conf_info_tuple[1] if conf_info_tuple[0] else {}

    @staticmethod
    def initLog():
        log_path = os.path.join(basedir, 'log')
        if not os.path.exists(log_path):
            os.makedirs(log_path)
        # 日志文件路径
        log_file = os.path.join(basedir, 'log', project_name + '.log')
        set_log_file(log_file)


eyes_conf = EyesConfig()
db_info = {
    "uri": eyes_conf.dt['me']['sqlalchemy_database_uri']
}

