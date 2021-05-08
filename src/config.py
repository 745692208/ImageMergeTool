import os
import configparser
import ctypes
from ctypes.wintypes import MAX_PATH


class Config:
    def make_conf_dir(self, name):
        # 获取我的文档路径，并创建目录
        dll = ctypes.windll.shell32
        buf = ctypes.create_unicode_buffer(MAX_PATH + 1)
        if dll.SHGetSpecialFolderPathW(None, buf, 0x0005, False):
            print(buf.value)
            try:
                os.mkdir(buf.value + r"\{}".format(name))
            except Exception:
                print("")
        else:
            print("Failure!")
        flie_path = buf.value + r"\{}\Config.ini".format(name)
        return flie_path


def read_config(config_file_path, field, key):
    cf = configparser.ConfigParser()
    try:
        cf.read(config_file_path)
        if field in cf:
            result = cf[field][key]
        else:
            return ''
    except configparser.Error as e:
        print(e)
        return ''
    return result


def write_config(config_file_path, field, key, value):
    cf = configparser.ConfigParser()
    try:
        cf.read(config_file_path)
        if field not in cf:
            cf.add_section(field)
        cf[field][key] = value
        cf.write(open(config_file_path, 'w'))
    except configparser.Error as e:
        print(e)
        return False
    return True


if __name__ == "__main__":
    print('test')
