import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
import webbrowser as web
import sys
import os

import config


class core:
    def __init__(self):
        self.path = ''


class App:
    def __init__(self):
        self.cf = config.Config('', 1, './')
        self.core = core()
        # GUI
        self.app = tk.Tk()
        self.app.title('图片合并工具 1.0.0')
        self.tab_index = tk.IntVar()
        self.tab_index.set(self.cf.load('base', 'tab_index', 0))
        self.entry_path = tk.StringVar()
        self.entry_path.set(self.cf.load('base', 'entry_path'))
        self.name = tk.StringVar()
        self.name.set(self.cf.load('base', 'name', 'new'))
        self.b_add_date = tk.IntVar()
        self.b_add_date.set(self.cf.load('base', 'b_add_date', '1'))
        self.b_DelOldFile = tk.IntVar()
        self.b_DelOldFile.set(self.cf.load('base', 'b_DelOldFile', '0'))
        self.b_OkOpen = tk.IntVar()
        self.b_OkOpen.set(self.cf.load('base', 'b_OkOpen', '1'))
        self.b_create_folder = tk.IntVar()
        self.b_create_folder.set(self.cf.load('base', 'b_create_folder', '1'))
        self.select_num_hint = tk.StringVar()
        self.select_num_hint.set('共选择：0 张图片')
        self.ftab_list = []
        self.create_widget()
        self.changeTab()

    def run(self):
        self.core


    def check_menu(self):
        web.open('https://github.com/745692208/ImageMergeTool')

    def select_files(self):
        files = filedialog.askopenfilenames(
            title="Select Image file",
            filetypes=(("Image", "*.png *.jpg *.psd"),)
        )
        self.select_images = files
        self.select_num_hint.set('共选择：{} 张图片'.format(len(files)))
        print(files)

    def browse(self):
        print('browse')
        dir = os.path.normpath(filedialog.askdirectory())
        if dir != '.':
            self.cf.save('base', 'entry_path', dir)
            self.entry_path.set(dir)

    def open_folder(self):
        try:
            os.startfile(self.entry_path.get())
        except Exception:
            messagebox.showerror("错误", "请输入正确的文件夹路径！")

    def changeTab(self):
        index = self.tab_index.get()
        self.cf.save('base', 'tab_index', str(index))
        self.lf_option.pack_forget()
        for ftab in self.ftab_list:
            ftab.pack_forget()
        self.ftab_list[index].pack(fill='x')
        self.lf_option.pack(side='top', fill='x')

    def create_widget(self):
        # GUI初始化
        menubar = tk.Menu(self.app)
        menubar.add_command(label='关于', command=self.check_menu)
        self.app['menu'] = menubar
        # 1 第0行 标签容器 创建标签
        fTab = tk.Frame(self.app)
        fTab.pack(side='top', fill='x')
        for i, name in enumerate(['选择图片', '选择文件夹']):
            ttk.Radiobutton(
                fTab, text=name, value=i,
                variable=self.tab_index, command=self.changeTab)\
                .pack(side='left')
        # 第一行 内容
        # 选择文件
        lf_select = ttk.LabelFrame(self.app, text='Select Image')
        lf_select.pack(side='top', fill='x')
        self.ftab_list.append(lf_select)
        tk.Label(lf_select, textvariable=self.select_num_hint, anchor='w')\
            .pack(side='left', fill='x', expand=1)
        ttk.Button(lf_select, text='选择文件', command=self.select_files)\
            .pack(side='left')
        # 路径
        lf_path = ttk.LabelFrame(self.app, text='Path')
        lf_path.pack(side='top', fill='x')
        self.ftab_list.append(lf_path)
        tk.Label(lf_path, text='文件夹路径：').pack(side='left')
        ttk.Entry(lf_path, textvariable=self.entry_path)\
            .pack(side='left', fill='x', expand=1)
        ttk.Button(lf_path, text='浏览', command=self.browse).pack(side='left')
        ttk.Button(lf_path, text='打开文件夹', command=self.open_folder)\
            .pack(side='left')
        # 第二行 选项
        self.lf_option = ttk.LabelFrame(self.app, text='Option')
        self.lf_option.pack(side='top', fill='x')

        f_name = ttk.Frame(self.lf_option)
        f_name.pack(side='top', fill='x')
        tk.Label(f_name, text='Name：').pack(side='left')
        ttk.Entry(f_name, textvariable=self.name)\
            .pack(side='left', fill='x', expand=1)
        ttk.Checkbutton(
            f_name, text='添加日期', variable=self.b_add_date,
            command=lambda: self.cf.save(
                'base', 'b_add_date', self.b_add_date.get()))\
            .pack(side='left')
        lf_cb = tk.Frame(self.lf_option)
        lf_cb.pack(side='top', fill='x')
        ttk.Checkbutton(
            lf_cb, text='删除旧文件', variable=self.b_DelOldFile,
            command=lambda: self.cf.save(
                'base', 'b_DelOldFile', self.b_DelOldFile.get()))\
            .pack(side='left')
        ttk.Checkbutton(
            lf_cb, text='创建New文件夹', variable=self.b_create_folder,
            command=lambda: self.cf.save(
                'base', 'b_create_folder', self.b_create_folder.get()))\
            .pack(side='left')
        ttk.Checkbutton(
            lf_cb, text='完成后打开文件夹', variable=self.b_OkOpen,
            command=lambda: self.cf.save(
                'base', 'b_OkOpen', self.b_OkOpen.get()))\
            .pack(side='left')
        lf_button = tk.Frame(self.lf_option)
        lf_button.pack(side='top', fill='x')
        # ttk.Button(lf_button, text='打开最后文件夹').pack(side='left')
        ttk.Button(lf_button, text='合并', command=self.run)\
            .pack(side='left', fill='both', expand=1)


if __name__ == '__main__':
    app = App()
    app.app.mainloop()
    app.app.quit()
    sys.exit()
