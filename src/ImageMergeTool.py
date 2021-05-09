# -*- coding: utf-8 -*-

"""
合并截图
"""

__version__ = "1.0.0"

from app import App


def main():
    app = App('图片合并工具', __version__, 'by:levosaber')  # 运行GUI
    app.create_widget()
    app.top.mainloop()  # 进入主循环，程序运行


if __name__ == '__main__':
    main()
