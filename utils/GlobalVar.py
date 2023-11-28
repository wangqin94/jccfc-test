import json

from utils.Logger import MyLog

_log = MyLog.get_log()


def _init():  # 初始化
    global data
    data = {}


def set_value(key, value):
    # 定义一个全局变量
    data[key] = value
    return data


def get_value(key):
    # 获得一个全局变量，不存在则提示读取对应变量失败
    try:
        return data[key]
    except KeyError:
        _log.info('读取' + key + '失败')


class GlobalMap:
    # 拼装成字典构造全局变量  借鉴map  包含变量的增删改查
    map = {}

    def set_map(self, key, value):
        if isinstance(value, dict):
            value = json.dumps(value)
        self.map[key] = value

    def set(self, **keys):
        try:
            for key_, value_ in keys.items():
                self.map[key_] = str(value_)
                _log.debug(key_ + ":" + str(value_))
        except BaseException as msg:
            _log.error(msg)
            raise msg

    def del_map(self, key):
        try:
            del self.map[key]
            return self.map
        except KeyError:
            raise "全局变量中不存在当前key:{}".format(key)

    def get(self, *args):
        try:
            dic = {}
            for key in args:
                if len(args) == 1:
                    dic = self.map[key]
                    _log.debug(key + ":" + str(dic))
                elif len(args) == 1 and args[0] == 'all':
                    dic = self.map
                else:
                    dic[key] = self.map[key]
            return dic
        except KeyError:
            raise "全局变量中不存在当前key:{}".format(args)
