# from tkinter import *
from tkinter import Tk, Label, Button, Entry  # Frame, Scrollbar, Text
from tkinter import Checkbutton, messagebox, filedialog
from tkinter import StringVar, EW, W, IntVar
# BOTTOM, TOP, LEFT, BOTH, X, Y, END, IntVar, BooleanVar

import os
import core
import config


class App:
    def cf_save(self, key, valur):
        self.cf.write_config(self.cf_path, 'base', key, str(valur))

    def cf_load(self, key):
        return self.cf.read_config(self.cf_path, 'base', key)

    def parma_get_cf(self, parma, key, value):
        cf_value = self.cf_load(key)
        if cf_value == '':
            parma.set(value)
        else:
            parma.set(cf_value)

    def save_all_parma(self):
        self.cf_save('entry_path', self.entry_path.get())
        self.cf_save('entry_name', self.entry_name.get())
        self.cf_save('cb_add_suffix', self.cb_add_suffix.get())
        self.cf_save('entry_suffix', self.entry_suffix.get())
        self.cf_save('cb_has_image_num', self.cb_has_image_num.get())
        self.cf_save('entry_image_num', self.entry_image_num.get())
        self.cf_save('cb_open_folder', self.cb_open_folder.get())
        self.cf_save('cb_del_old_image', self.cb_del_old_image.get())
        self.cf_save('cb_date_sort', self.cb_date_sort.get())

    def select_dir(self):
        dir = filedialog.askdirectory()
        if dir:
            self.entry_path.set(dir)  # 设置tk的变量
            self.save_all_parma()

    def open_folder(self):
        try:
            os.startfile(self.entry_path.get())
        except Exception:
            messagebox.showerror("错误", "请输入正确的文件夹路径")

    def run(self):
        print('run')
        self.save_all_parma()
        self.core.image_merge(
            self.entry_path.get(),
            self.entry_name.get(),
            self.cb_add_suffix.get(),
            self.entry_suffix.get(),
            self.cb_has_image_num.get(),
            self.entry_image_num.get(),
            self.cb_open_folder.get(),
            self.cb_del_old_image.get(),
            self.cb_date_sort.get(),
        )

    def create_widget(self):
        self.entry_path = StringVar()
        self.parma_get_cf(self.entry_path, 'entry_path', '')
        self.entry_name = StringVar()
        self.parma_get_cf(self.entry_name, 'entry_name', 'New')
        self.cb_add_suffix = IntVar()
        self.parma_get_cf(self.cb_add_suffix, 'cb_add_suffix', 1)
        self.entry_suffix = StringVar()
        self.parma_get_cf(self.entry_suffix, 'entry_suffix', '01')
        self.cb_has_image_num = IntVar()
        self.parma_get_cf(self.cb_has_image_num, 'cb_has_image_num', 0)
        self.entry_image_num = StringVar()
        self.parma_get_cf(self.entry_image_num, 'entry_image_num', '')
        self.cb_open_folder = IntVar()
        self.parma_get_cf(self.cb_open_folder, 'cb_open_folder', 1)
        self.cb_del_old_image = IntVar()
        self.parma_get_cf(self.cb_del_old_image, 'cb_del_old_image', 0)
        self.cb_date_sort = IntVar()
        self.parma_get_cf(self.cb_date_sort, 'cb_date_sort', 0)

        # ===============创建控件===============
        Label(text='文件夹路径：').grid(row=0, column=0)
        Entry(textvariable=self.entry_path).grid(row=0, column=1)
        Button(text='浏览', command=self.select_dir)\
            .grid(row=0, column=2, sticky=EW)

        Label(text='新名字：').grid(row=1, column=0)
        Entry(textvariable=self.entry_name).grid(row=1, column=1)

        Checkbutton(text='删除旧图', variable=self.cb_del_old_image,
                    command=self.save_all_parma)\
            .grid(row=1, column=2, sticky=W)
        Checkbutton(text='按日期排序', variable=self.cb_date_sort,
                    command=self.save_all_parma)\
            .grid(row=2, column=2, sticky=W)
        Checkbutton(text='打开文件夹', variable=self.cb_open_folder,
                    command=self.save_all_parma)\
            .grid(row=3, column=2, sticky=W)

        Checkbutton(text='加入尾缀', variable=self.cb_add_suffix,
                    command=self.save_all_parma)\
            .grid(row=2, column=0, sticky=W)
        Entry(textvariable=self.entry_suffix).grid(row=2, column=1, sticky=W)

        Checkbutton(text='限制图片数量', variable=self.cb_has_image_num,
                    command=self.save_all_parma)\
            .grid(row=3, column=0, sticky=W)
        Entry(textvariable=self.entry_image_num)\
            .grid(row=3, column=1, sticky=W)

        Button(text='打开文件夹', command=self.open_folder)\
            .grid(row=4, column=0, sticky=EW)
        Button(text='执行合并', command=self.run).grid(row=4, column=1, sticky=EW)

    def __init__(self, name, version, suffix):
        self.core = core.Core()
        self.top = Tk()
        self.top.title('{} {} {}'.format(name, version, suffix))   # 设置标题名字
        self.top.iconbitmap(r'.\icon\icon.ico')
        self.cf = config.Config()
        self.cf_path = self.cf.make_conf_dir(name)
        self.create_widget()


if __name__ == '__main__':
    app = App('GUI', 'Test', '')
    app.top.mainloop()
