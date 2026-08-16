from tkinter import ttk
from tkinter import filedialog, messagebox
import tkinter as tk
import webbrowser as web
import time
import sys
import os
import re
import json

import PIL.Image as Image
import windnd  # pip install windnd

import ctypes
from ctypes.wintypes import MAX_PATH


# ==================== Config (JSON) ====================
class Config:
    def __init__(self, title="", bIsCustomPath=0, dirpath="./"):
        self.title = title
        self.flag = bIsCustomPath
        self.dirpath = dirpath

        # 配置文件路径，如: ./ImageMergeTool.json
        if bIsCustomPath:
            filename = f"{title}.json" if title else "config.json"
            self._filepath = os.path.join(dirpath, filename)
        else:
            self._filepath = self.make_conf_dir(title)

        self._data = {}
        self._read()

    def make_conf_dir(self, name="") -> str:
        # 获取我的文档路径，并创建目录
        directory_name = "LS_Toolkit"
        dll = ctypes.windll.shell32
        buf = ctypes.create_unicode_buffer(MAX_PATH + 1)
        if dll.SHGetSpecialFolderPathW(None, buf, 0x0005, False):
            print(buf.value)
            try:
                os.mkdir(f"{buf.value}\\{directory_name}")
            except Exception as e:
                print(e)
        else:
            print("Failure!")
        flie_path = f"{buf.value}\\{directory_name}\\{name}.json"
        return flie_path

    def get_filepath(self):
        return self._filepath

    def _read(self):
        """从磁盘读取整个 json"""
        if os.path.exists(self._filepath):
            try:
                with open(self._filepath, "r", encoding="utf-8") as f:
                    self._data = json.load(f)
            except (json.JSONDecodeError, OSError):
                self._data = {}
        else:
            self._data = {}

    def _write(self):
        """把内存数据写入磁盘"""
        try:
            with open(self._filepath, "w", encoding="utf-8") as f:
                json.dump(self._data, f, ensure_ascii=False, indent=4)
        except OSError as e:
            print(f"[Config] 写入失败: {e}")

    def load(self, section, key, default=None):
        """读取配置。兼容: cf.load("base", "name", "New")"""
        return self._data.get(section, {}).get(key, default)

    def save(self, section, key, value):
        """保存配置并立即写入磁盘。兼容: cf.save("base", "name", "New")"""
        if section not in self._data:
            self._data[section] = {}
        self._data[section][key] = value
        self._write()


# ==================== 工具函数 ====================
def _natural_key(s):
    """自然排序 key: New1, New2, New10 而不是 New1, New10, New2"""
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", s)]


# ==================== 核心逻辑 ====================
class core:
    def __init__(self):
        self.cf: Config = None
        pass

    def convert_image_path(self, image_path_list) -> list:
        """[filepath] -> [filename]"""
        a = []
        for s in image_path_list:
            a.append(s.rsplit("/", 1)[1])
        return a

    def get_dir_images_path(self, path) -> list[str]:
        """找到文件夹里支持格式的图片名字, 如: ["yangchen0927-485gn2-1.jpg", ]"""
        return os.listdir(path)

    def merge_image(self, dirpath, image_names, name, b_OkOpen, b_DelOldFile, b_create_folder, b_add_date, b_add_index, format="jpg", quality=95):
        """
        ::param dirpath: "d:/test"
        ::param image_names 图片的名字: "name.png"
        ::param name 合成后图片的名字
        """
        # 防止没有图片或图片太少问题
        if len(image_names) < 2:
            messagebox.showerror("错误", "请确认好选择的内容.\n选择图片的总数, 必须大于1张.")
            return
        # 创建new文件夹并设置path
        save_dirpath = dirpath
        if b_create_folder:
            save_dirpath = os.path.join(save_dirpath, "New")
            os.makedirs(save_dirpath, exist_ok=True)
        # 新图片名字添加日期
        if b_add_date:
            time_date = time.strftime("%y-%m-%d")
            name = f"{name}_{time_date}"
        if b_add_index:
            index = 1
            new_filename = f"{name}_{index:02d}"
            while os.path.exists(os.path.join(save_dirpath, f"{new_filename}.{format}")):
                index += 1
                new_filename = f"{name}_{index:02d}"
            name = new_filename
        # 获取所有图片高度并得出最高的图片
        image_objs = [Image.open(os.path.join(dirpath, n)) for n in image_names]
        size_y = max([i.size[1] for i in image_objs])
        # resize所有图片，等比放大，并计算宽度总和
        for i, im in enumerate(image_objs):
            ratio = size_y / im.size[1]
            image_objs[i] = im.resize((int(im.size[0] * ratio), int(im.size[1] * ratio)))
        size_x_list = [i.size[0] for i in image_objs]
        size_x = 0
        # 合成图片并保存
        new_image = Image.new("RGB", (sum(size_x_list), size_y))  # 创建一个新图
        for i, image in enumerate(image_objs):
            new_image.paste(image, (size_x, 0))
            size_x += image.size[0]
        # 保存图片
        new_image.save(os.path.join(save_dirpath, f"{name}.{format}"), quality=quality)  # 保存图片, 如: d:\asd\1.jpg
        # 打开合并图片所在地
        if b_OkOpen:
            os.startfile(save_dirpath)
        # 删除旧文件
        if b_DelOldFile:
            for n in image_names:
                os.remove(os.path.join(dirpath, n))

    def separator_rgb(self, img_path: str):
        dirpath, name = os.path.split(img_path)
        name, ext = os.path.splitext(name)
        # 打开图像
        img = Image.open(img_path)
        rgb_im = img.convert("RGBA")  # 如果图片已经是RGB模式则无需此步骤
        # 分离RGB通道
        channels = rgb_im.split()
        # 保存分离后的通道为单独的图像文件
        suffix = ["R", "G", "B", "A"]
        for i, c in enumerate(channels):
            savepath = os.path.join(dirpath, f"{name}_{suffix[i]}{ext}")
            c.save(savepath)


# ==================== GUI ====================
class App:
    def __init__(self, title, ver, suffix):
        self.cf = Config(title, 0, "./")
        self.core = core()
        self.core.cf = self.cf
        # GUI
        self.app = tk.Tk()
        self.app.title(f"{title} {ver} {suffix}")
        self.app.minsize(350, 0)  # 设置最低size
        self.tab_index = tk.IntVar()
        self.tab_index.set(int(self.cf.load("base", "tab_index", 0)))
        # Options
        self.name = tk.StringVar()
        self.name.set(self.cf.load("base", "name", "New"))
        # 名字列表（JSON 里直接存为 list）
        name_list = self.cf.load("base", "name_list", ["New"])
        if isinstance(name_list, str):  # 兼容旧的 "|" 分隔字符串
            name_list = [n for n in name_list.split("|") if n]
        self.name_list = name_list if name_list else ["New"]
        self.name_list = sorted(set(self.name_list), key=_natural_key)  # 去重+自然排序

        self.topmost_var = tk.BooleanVar(value=False)
        self.topmost_var.set(int(self.cf.load("base", "topmost_var", 0)))
        self.b_add_date = tk.IntVar()
        self.b_add_date.set(int(self.cf.load("base", "b_add_date", 1)))
        self.b_add_index = tk.IntVar()
        self.b_add_index.set(int(self.cf.load("base", "b_add_index", 1)))
        self.b_DelOldFile = tk.IntVar()
        self.b_DelOldFile.set(int(self.cf.load("base", "b_DelOldFile", 0)))
        self.b_OkOpen = tk.IntVar()
        self.b_OkOpen.set(int(self.cf.load("base", "b_OkOpen", 1)))
        self.b_create_folder = tk.IntVar()
        self.b_create_folder.set(int(self.cf.load("base", "b_create_folder", 1)))
        # 格式下拉框（默认 JPG）
        self.format = tk.StringVar()
        self.format.set(self.cf.load("base", "format", "JPG"))
        self.select_num_hint = tk.StringVar()
        self.select_num_hint.set("共选择: 0 张图片")
        self.select_images = []
        self.ftab_list = []
        self.create_widget()
        self.on_change_tab()
        # 绑定拖入事件
        windnd.hook_dropfiles(self.app, self.on_dropfile, True)
        self.app.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        # Save data
        self.cf.save("base", "name", self.name.get())
        self.cf.save("base", "name_list", self.name_list)  # 直接存 list
        self.cf.save("base", "b_OkOpen", self.b_OkOpen.get())
        self.cf.save("base", "tab_index", self.tab_index.get())
        self.cf.save("base", "b_add_date", self.b_add_date.get())
        self.cf.save("base", "b_add_index", self.b_add_index.get())
        self.cf.save("base", "b_DelOldFile", self.b_DelOldFile.get())
        self.cf.save("base", "b_create_folder", self.b_create_folder.get())
        self.cf.save("base", "format", self.format.get())
        self.cf.save("base", "topmost_var", self.topmost_var.get())

        # Exit
        self.app.quit()
        sys.exit()

    def on_open_config(self):
        path = self.cf.get_filepath()
        if os.path.exists(path):
            os.startfile(path)

    def on_about(self):
        web.open("https://github.com/745692208/ImageMergeTool")

    def on_change_tab(self):
        index = self.tab_index.get()
        for ftab in self.ftab_list:
            ftab.pack_forget()
        self.ftab_list[index].pack(side="top", fill="both", expand=1)

    def on_select_files(self):
        files = filedialog.askopenfilenames(title="Select Image file", filetypes=(("Image", "*.png *.jpg"),))
        self.select_images = files
        self.select_num_hint.set(f"共选择: {len(files)} 张图片")
        print(files)

    def on_dropfile(self, ls):
        print(ls)
        ls = [i.decode("gbk").replace("\\", "/") if isinstance(i, bytes) else i.replace("\\", "/") for i in ls]
        ls.sort()
        self.select_images = ls
        self.on_run()

    def on_add_name(self):
        """把当前输入框的名字添加到下拉列表"""
        name = self.name.get().strip()
        if not name:
            messagebox.showwarning("提示", "名字不能为空")
            return
        if name in self.name_list:
            messagebox.showinfo("提示", "该名字已存在")
            return
        self.name_list.append(name)
        self.name_list = sorted(set(self.name_list), key=_natural_key)  # 自然排序
        self.name_combobox["values"] = self.name_list

    def on_del_name(self):
        """从下拉列表删除当前名字"""
        name = self.name.get().strip()
        if name in self.name_list:
            self.name_list.remove(name)
            self.name_list = sorted(set(self.name_list), key=_natural_key)  # 自然排序
            self.name_combobox["values"] = self.name_list
            # 删除后自动选中列表中的第一个（如果还有）
            if self.name_list:
                self.name.set(self.name_list[0])
            else:
                self.name.set("")
        else:
            messagebox.showinfo("提示", "列表中没有该名字")

    def on_run(self):
        filepaths = [i for i in self.select_images if os.path.isfile(i)]
        dirpaths = [i for i in self.select_images if os.path.isdir(i)]
        if self.tab_index.get() == 0:
            # file path
            if filepaths:
                names = self.core.convert_image_path(filepaths)
                dirpath = self.select_images[0].rsplit("/", 1)[0]
                self.merge_image(dirpath, names)
            # dir path
            for path in dirpaths:
                names = self.core.get_dir_images_path(path)
                self.merge_image(path, names)
        elif self.tab_index.get() == 1:
            if filepaths:
                [self.core.separator_rgb(i) for i in filepaths]
            for path in dirpaths:
                names = self.core.get_dir_images_path(path)
                dir_filepaths = [os.path.join(path, n) for n in names]
                [self.core.separator_rgb(i) for i in dir_filepaths]

    def merge_image(self, dirpath, names):
        # 根据下拉框选择决定格式
        fmt = "jpg" if self.format.get().upper() == "JPG" else "png"
        self.core.merge_image(
            dirpath,
            names,
            self.name.get(),
            self.b_OkOpen.get(),
            self.b_DelOldFile.get(),
            self.b_create_folder.get(),
            self.b_add_date.get(),
            self.b_add_index.get(),
            fmt,
        )

    def toggle_topmost(self):
        # 获取当前状态并取反
        self.app.attributes("-topmost", self.topmost_var.get())

    def create_widget(self):
        # GUI初始化
        menubar = tk.Menu(self.app)
        options = tk.Menu(menubar, tearoff=0)
        options.add_command(label="Open.ini", command=self.on_open_config)
        options.add_command(label="About", command=self.on_about)
        menubar.add_cascade(label="可拖入图片文件或图片文件夹", menu=options)
        self.app["menu"] = menubar
        # 第零行 标签容器 and 创建标签
        fTab = tk.Frame(self.app)
        fTab.pack(side="top", fill="x")
        for i, name in enumerate(["合并图片", "分离颜色通道"]):
            ttk.Radiobutton(fTab, text=name, value=i, variable=self.tab_index, command=self.on_change_tab).pack(side="left")

        # 置顶
        self.pin_chk = tk.Checkbutton(fTab, text="📌", variable=self.topmost_var, command=self.toggle_topmost)
        self.pin_chk.pack(side="right")

        # Tab 1 合并图片
        # 第一行 选择图片
        tab1_0 = ttk.Frame(self.app)
        tab1_0.pack(side="top", fill="x")
        self.ftab_list.append(tab1_0)
        tab1_1_select = ttk.LabelFrame(tab1_0, text="Select Images")
        tab1_1_select.pack(side="top", fill="x")
        tk.Label(tab1_1_select, textvariable=self.select_num_hint, anchor="w").pack(side="left", fill="x", expand=1)
        ttk.Button(tab1_1_select, text="选择文件", command=self.on_select_files).pack(side="left")
        # 第二行 选项
        tab1_2_options = ttk.LabelFrame(tab1_0, text="Option")
        tab1_2_options.pack(side="top", fill="both", expand=1)
        f_name = ttk.Frame(tab1_2_options)
        f_name.pack(side="top", fill="x")
        tk.Label(f_name, text="名字: ").pack(side="left")
        # 可编辑下拉框：既能手动输入，也能从列表选择
        self.name_combobox = ttk.Combobox(f_name, textvariable=self.name, values=self.name_list)
        self.name_combobox.pack(side="left", fill="x", expand=1)
        ttk.Button(f_name, text="+", width=2, command=self.on_add_name).pack(side="left")
        ttk.Button(f_name, text="-", width=2, command=self.on_del_name).pack(side="left")
        # 选项第二行
        row = tk.Frame(tab1_2_options)
        row.pack(side="top", fill="x")
        # 格式下拉框（只读，不允许手动输入，默认 JPG）
        ttk.Label(row, text="格式: ").pack(side="left")
        self.format_combobox = ttk.Combobox(row, textvariable=self.format, values=["JPG", "PNG"], width=5, state="readonly")
        self.format_combobox.pack(side="left")
        # 其它
        ttk.Checkbutton(row, text="添加日期", variable=self.b_add_date).pack(side="left")
        ttk.Checkbutton(row, text="添加序号", variable=self.b_add_index).pack(side="left")
        # 选项第三行
        lf_cb = tk.Frame(tab1_2_options)
        lf_cb.pack(side="top", fill="x")
        ttk.Checkbutton(lf_cb, text="删除旧文件", variable=self.b_DelOldFile).pack(side="left")
        ttk.Checkbutton(lf_cb, text="创建New文件夹", variable=self.b_create_folder).pack(side="left")
        ttk.Checkbutton(lf_cb, text="完成后打开文件夹", variable=self.b_OkOpen).pack(side="left")

        lf_button = tk.Frame(tab1_2_options)
        # lf_button.pack(side="bottom", fill="both", expand=1)
        lf_button.pack(fill="both", expand=1)
        ttk.Button(lf_button, text="合并", command=self.on_run).pack(fill="both", expand=1)

        # ==================== Tab 2 分离颜色通道 ====================
        tab2 = ttk.Frame(self.app)
        tab2.pack(side="top", fill="both", expand=1)
        self.ftab_list.append(tab2)
        tab2_hint = ttk.LabelFrame(tab2, text="分离颜色通道")
        tab2_hint.pack(fill="both", expand=1)
        ttk.Label(tab2_hint, text="拖入图片或文件夹即可分离 RGBA 通道").pack(pady=6)
        ttk.Button(tab2_hint, text="选择图片并分离", command=self._run_separate).pack(fill="both", expand=1)

    def _run_separate(self):
        files = filedialog.askopenfilenames(title="Select Image file", filetypes=(("Image", "*.png *.jpg"),))
        for f in files:
            self.core.separator_rgb(f.replace("\\", "/"))
        if files:
            messagebox.showinfo("完成", "通道分离完成")

    def run(self):
        self.app.mainloop()


if __name__ == "__main__":
    app = App("ImageMergeTool", "2.4.1", "")
    app.run()
