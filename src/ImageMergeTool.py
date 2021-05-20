from tkinter import ttk
from tkinter import filedialog, messagebox
import tkinter as tk
import webbrowser as web
import time
import sys
import os

import PIL.Image as Image
import config


class core:
    def __init__(self):
        self.cf = config.Config('', 1, '')
        self.path = ''
        self.image_format = ['.png', '.PNG', '.jpg', '.JPG']

    def convert_image_path(self, image_path_list):
        a = []
        for str in image_path_list:
            a.append(str.rsplit('/', 1)[1])
        return a

    def get_dir_images_path(self, path):
        '''输出：yangchen0927-485gn2-1.jpg'''
        try:
            image_names = [
                name for name in os.listdir(path) for item in self.image_format
                if os.path.splitext(name)[1] == item
            ]
        except Exception as e:
            print("没有找到文件夹", e)
            messagebox.showerror("错误", "请输入正确的文件夹路径")
            return
        return image_names

    def merge_image(
            self, path, images_path, name,
            b_OkOpen, b_DelOldFile, b_create_folder, b_add_date):
        # 防止没有图片或图片太少问题
        if len(images_path) < 2:
            messagebox.showerror("错误", "路径里没有合适的图片")
            return
        # 创建new文件夹并设置path
        path = path + '\\'
        save_path = path
        if b_create_folder:
            save_path = os.path.join(path, 'new\\')
            os.makedirs(save_path, exist_ok=True)
            # self.cf.save('base', 'latest_path', path)
        print('最终路径', path)
        # 新图片名字添加日期
        if b_add_date:
            time_date = time.strftime("%y-%m-%d")
            name = '{}_{}.jpg'.format(name, time_date)
        else:
            name = '{}.jpg'.format(name)
        # 合成图片
        print(path + name)
        image_num = len(images_path)  # 获取总图片数量
        image_size = Image.open(path + images_path[0]).size  # 获取第一张图大小
        new_image = Image.new(
            'RGB', (image_size[0] * image_num, image_size[1]))  # 创建一个新图
        for i, image in enumerate(images_path):
            image_obj = Image.open(path + image)
            new_image.paste(image_obj, (i * image_size[0], 0))
        new_image.save(save_path + name)  # 保存图片，如：d:\asd\1.jpg
        # 打开合并图片所在地
        if b_OkOpen:
            os.startfile(save_path)
        # 删除旧文件
        if b_DelOldFile:
            for image in images_path:
                os.remove(path + image)


class App:
    def __init__(self, title, ver, suffix):
        self.cf = config.Config(title, 0, './')
        self.core = core()
        self.core.cf = self.cf
        # GUI
        self.app = tk.Tk()
        self.app.title('{} {} {}'.format(title, ver, suffix))
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

    def merge_image(self, images, path):
        self.core.merge_image(
            path, images, self.name.get(),
            self.b_OkOpen.get(), self.b_DelOldFile.get(),
            self.b_create_folder.get(), self.b_add_date.get()
        )

    def run(self):
        self.cf.save('base', 'entry_path', self.entry_path.get())
        self.cf.save('base', 'name', self.name.get())
        if self.tab_index.get() == 0:
            images = self.core.convert_image_path(self.select_images)
            self.merge_image(images, self.select_images[0].rsplit('/', 1)[0])
        elif self.tab_index.get() == 1:
            images = self.core.get_dir_images_path(self.entry_path.get())
            self.merge_image(images, self.entry_path.get())

    def check_menu(self):
        web.open('https://github.com/745692208/ImageMergeTool')

    def select_files(self):
        files = filedialog.askopenfilenames(
            title="Select Image file",
            filetypes=(("Image", "*.png *.jpg"),)
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
        f_path = tk.Frame(lf_path)
        f_path.pack(side='top', fill='x')
        self.ftab_list.append(lf_path)
        tk.Label(f_path, text='文件夹路径：').pack(side='left')
        ttk.Entry(f_path, textvariable=self.entry_path, width=50)\
            .pack(side='left', fill='x', expand=1)
        ttk.Button(f_path, text='浏览', command=self.browse)\
            .pack(side='left')
        ttk.Button(lf_path, text='打开文件夹', command=self.open_folder)\
            .pack(side='left', fill='x', expand=1)
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
    app = App('ImageMergeTool', '2.0.0', '')
    app.app.mainloop()
    app.app.quit()
    sys.exit()
