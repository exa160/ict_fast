import json
import os.path

from logger import *

if getattr(sys, 'frozen', False):  # 打包静态资源问题
    base_path = sys._MEIPASS
else:
    # base_path = os.path.abspath(".")
    base_path = os.path.dirname(os.path.realpath(sys.argv[0]))

cur_path = os.path.dirname(os.path.realpath(sys.argv[0]))


class AttrDict(dict):
    def __getattr__(self, item):
        return self.get(item, '')

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        del self[key]


class ConfigAttrDict(AttrDict):
    def __init__(self, config_file=r'config.json', _config=None):
        super().__init__()
        _config_path = os.path.join(cur_path, config_file)
        self.config_path = _config_path
        if os.path.exists(_config_path):
            _config = self.read_config()
            if _config.get('debug', False):
                _config = {}
        elif _config is None:
            _config = {}
        # else:
        # self._config = _config
        self.dict_init(_config)
        self.config_init(config_file, _config)

    def dict_init(self, dict_data):
        for key, values in dict_data.items():
            self[key] = values

    # @staticmethod
    def config_init(self, config_file, _config=None):
        """
        初始化配置文件
        :param config_file:配置文件名
        :param _config:dict
        :return:
        """
        if _config is None:
            _config = {}

        with open(config_file, 'w') as c:
            json.dump(_config, c, indent=4, ensure_ascii=False)
        self.config_path = config_file

    def get_config(self):
        # return AttrDict(self._config)
        return self

    def read_config(self):
        """
        获取配置信息
        :return: _config: AttrDict
        """
        with open(self.config_path, 'r') as c:
            _config = json.load(c)
        return AttrDict(_config)

    def save(self, config_file=None, _config=None):
        """
        保存配置文件
        :param config_file:
        :param _config:
        :return:
        """
        if config_file is None:
            config_file = self.pop('config_path')
        if _config is None:
            _config = self
        try:
            self.config_init(config_file, _config)
        except Exception as e:
            print(e)


config_path = os.path.join(base_path, 'data.cfg')
config = ConfigAttrDict(config_path, {'debug': True,
                                      'table': {}})

logger = logger_init(config.debug)

if __name__ == '__main__':
    print(config)
