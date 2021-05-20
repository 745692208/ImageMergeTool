# 2021年5月20日 01:19:08
import os
import configparser
import ctypes
from ctypes.wintypes import MAX_PATH


class Config:
    def load(self, field, key, *failValue):
        ''':param *failValue, None, 读取失败后，返回的值。默认返回'';'''
        if len(failValue) == 0:
            failValue = ''
        else:
            failValue = failValue[0]
        cf = configparser.ConfigParser()
        try:
            cf.read(self.path, encoding="utf-8")
            if field in cf:
                result = cf.get(field, key)
                print('load-{}-{}'.format(field, key))
            else:
                print('读取失败，不存在field')
                return failValue
        except Exception as e:
            print(e)
            print('读取失败')
            return failValue
        return result

    def save(self, field, key, value):
        cf = configparser.ConfigParser()
        value = str(value)
        try:
            cf.read(self.path, encoding="utf-8")
            if field not in cf:
                cf.add_section(field)
            cf.set(field, key, value)
            cf.write(open(self.path, "w", encoding="utf-8"))
            print('save-{}-{}-{}'.format(field, key, value))
        except Exception as e:
            print(e)
            print('写入失败')
            return False
        return True

    def make_conf_dir(self, name):
        # 获取我的文档路径，并创建目录
        dll = ctypes.windll.shell32
        buf = ctypes.create_unicode_buffer(MAX_PATH + 1)
        if dll.SHGetSpecialFolderPathW(None, buf, 0x0005, False):
            print(buf.value)
            try:
                os.mkdir(buf.value + r"\{}".format(name))
            except Exception as e:
                print(e)
                print("")
        else:
            print("Failure!")
        flie_path = buf.value + r"\{}\Config.ini".format(name)
        return flie_path

    def get_cf(self):
        cf = configparser.ConfigParser()
        cf.read(self.path, encoding="utf-8")
        return cf

    def sections(self):
        cf = self.get_cf()
        return cf.sections()

    def options(self, sections):
        cf = self.get_cf()
        return cf.options(sections)

    def get_all(self):
        cf = self.get_cf()
        cf_data = {}
        for section in cf.sections():
            cf_data[section] = {}
            for option in cf.options(section):
                cf_data[section][option] = self.load(section, option)
        return cf_data

    def __init__(self, name, bIsCustomPath, *custom_path) -> None:
        '''Config
        :param name, str, 默认文件夹和ini的名字。
        :param bIsCustomPath, bool, 是否使用特定的ini保存路径，不使用的话会保持在我的文档里。
        :param *custom_path, str, 使用上面的参数后，这里需要输入自定义保存的路径。'''
        self.cf = configparser.ConfigParser()
        if bIsCustomPath:
            self.path = custom_path[0] + name + '.ini'
        else:
            self.path = self.make_conf_dir(name)
            print(self.path)


if __name__ == "__main__":
    print('test')
    cf = Config('test', True, './')
    cf.save('a', 'key', 'valur')
    cf.load('a', 'key')
    print(cf.load('b', 'key'))
