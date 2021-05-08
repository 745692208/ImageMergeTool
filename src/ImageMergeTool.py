from tkinter import *   #https://docs.python.org/3/library/tk.html、https://www.runoob.com/python/python-gui-tkinter.html
import tkinter.filedialog   #https://docs.python.org/3/library/dialog.html#module-tkinter.filedialog
import tkinter.messagebox   #https://docs.python.org/3/library/tkinter.messagebox.html
import PIL.Image as Image   # https://pillow-cn.readthedocs.io/zh_CN/latest/
import configparser
import os
import time
import sys
import ctypes
from ctypes.wintypes import MAX_PATH

# 获取我的文档路径，并创建目录
dll = ctypes.windll.shell32
buf = ctypes.create_unicode_buffer(MAX_PATH + 1)
if dll.SHGetSpecialFolderPathW(None, buf, 0x0005, False):
    print(buf.value)
    try:
        os.mkdir(buf.value + "\ImageMergeTool")
    except:
        print("")
else:
    print("Failure!")

# ===============全局变量===============
flie_path = buf.value + "\ImageMergeTool\Config.ini"

# ===============函数===============
def cp_set(option,var):  #写入
    global inifile
    inifile.set('base',option,var)
    inifile.write(open(flie_path, "w", encoding="utf-8"))

#控件变量save
def tk_path_save(*args):
    cp_set('tk_path',tk_path.get())
def tk_name_save(*args):
    cp_set('tk_name',tk_name.get())
def tk_image_num_save(*args):
    cp_set('tk_image_num',tk_image_num.get())
def tk_suffix_save(*args):
    cp_set('tk_suffix',tk_suffix.get())
def tk_open_folder_save():
    cp_set('tk_open_folder',str(int(tk_open_folder.get())))
def tk_del_old_image_save():
    cp_set('tk_del_old_image',str(int(tk_del_old_image.get())))
def tk_has_image_num_save():
    cp_set('tk_has_image_num',str(int(tk_has_image_num.get())))
def tk_date_sort_save():
    cp_set('tk_date_sort',str(int(tk_date_sort.get())))    
def tk_add_suffix_save():
    cp_set('tk_add_suffix',str(int(tk_add_suffix.get())))   

#控件相关
def select_dir():
    tk_path.set(tkinter.filedialog.askdirectory())  #设置tk的变量
    cp_set('tk_path',tk_path.get()) #写入配置

def open_folder():
    try:
        os.startfile(tk_path.get() + r"\new")
    except:
        message = tkinter.messagebox.showerror("错误", "请输入正确的文件夹路径")

def run():
    print("开始")
    image_format = ['.png','.PNG','.jpg','.JPG'] # 图片格式
    image_path = tk_path.get() + '/'
    new_image_name = tk_name.get()
    suffix = tk_suffix.get()
    image_column = tk_image_num.get()  # 图片间隔，也就是合并成一张图后，一共有几列
    bIsOpenFold = tk_open_folder.get()
    bIsRemoveOldImage = tk_del_old_image.get()
    # 获取图片并判断名字和数量
    try:
        image_names = [name for name in os.listdir(image_path) for item in image_format if os.path.splitext(name)[1] == item]
    except:
        print("没有找到文件夹")
        message = tkinter.messagebox.showerror("错误", "请输入正确的文件夹路径")
        pass
    print(image_names)
    image_column = len(image_names)
    print(tk_date_sort.get())
    if tk_date_sort.get():
        print("按日期排序")
        image_names = sorted(image_names, key=lambda x: os.path.getmtime(os.path.join(image_path, x)))   #按日期排序
    #else:
        #image_names = sorted(image_names)   #按名字排序
    if tk_has_image_num.get():
        image_column = int(tk_image_num.get())
        image_names = image_names[len(image_names) - image_column : len(image_names)]   #排除多余贴图
    print(image_names)
    # 获取第一张图片的大小
    print(image_path + image_names[0])
    image_size = Image.open(image_path + image_names[0]).size
    # 创建与合并图片， 参考：https://www.cnblogs.com/gisoracle/p/12081967.html
    new_image = Image.new('RGB', (image_size[0] * image_column, image_size[1]))  # 创建一个新图
    for i in range(0, image_column):
        image_obj = Image.open(image_path + image_names[i])
        new_image.paste(image_obj, (i * image_size[0], 0))
    # 创建目录
    if os.path.exists(image_path + "new") == 0:
        os.mkdir(image_path + "new")
    # 保存图片
    if tk_add_suffix.get():
        new_image.save(image_path + "new//" + new_image_name + "_" + time.strftime("%y-%m-%d") + "_" + suffix + ".png")  # 保存新图
    else:
        new_image.save(image_path + "new//" + new_image_name + "_" + time.strftime("%y-%m-%d") + ".png")  # 保存新图 没有后缀
    # 打开文件夹
    if bIsOpenFold:
        os.startfile(image_path + "new/")
    # 删除旧文件
    if bIsRemoveOldImage:
        for i in image_names:
            os.remove(image_path + i)
    print("执行完成!")

# ===============Run===============
# configparser 初始化
# 没有文件就创建
if os.path.exists(flie_path) == 0:
    print("没找到ini，创建一个新文件")
    inifile = open(flie_path, "w", encoding="utf-8")

inifile = configparser.ConfigParser()    # 初始化
inifile.read(flie_path, encoding="utf-8")
if not inifile.has_section('base'):  # 检查是否存在section
    inifile.add_section("base")
    inifile.set('base','tk_path','请输入文件夹路径')
    inifile.set('base','tk_name','New')
    inifile.set('base','tk_open_folder','1')
    inifile.set('base','tk_del_old_image','0')
    inifile.set('base','tk_image_num','4')
    inifile.set('base','tk_has_image_num','0')
    inifile.set('base','tk_date_sort','0')
    inifile.set('base','tk_suffix','01')
    inifile.set('base','tk_add_suffix','1')
    inifile.write(open(flie_path, "w", encoding="utf-8"))

# ===============创建GUI===============
top = Tk()  #创建GUI
top.title('图片合并工具v1.0 by levosaber')   #设置标题名字
top.geometry('340x150+1000+300')    #设置窗口大小、位置

# TK的变量和python的变量不同，因为要实时追踪相关原因，必须在Tk()函数下才能使用
tk_path = StringVar()
tk_path.set(inifile.get('base','tk_path'))
tk_path.trace_add('write', tk_path_save)

tk_name = StringVar()
tk_name.set(inifile.get('base','tk_name'))
tk_name.trace_add('write', tk_name_save)

tk_image_num = StringVar()
tk_image_num.set(inifile.get('base','tk_image_num'))
tk_image_num.trace_add('write', tk_image_num_save)

tk_suffix = StringVar()
tk_suffix.set(inifile.get('base','tk_suffix'))
tk_suffix.trace_add('write', tk_suffix_save)

tk_open_folder = BooleanVar()
tk_open_folder.set(inifile.get('base','tk_open_folder'))

tk_del_old_image = BooleanVar()
tk_del_old_image.set(inifile.get('base','tk_del_old_image'))

tk_has_image_num = BooleanVar()
tk_has_image_num.set(inifile.get('base','tk_has_image_num'))

tk_date_sort = BooleanVar()
tk_date_sort.set(inifile.get('base','tk_date_sort'))

tk_add_suffix = BooleanVar()
tk_add_suffix.set(inifile.get('base','tk_add_suffix'))



# ===============创建控件===============
Label(text='文件夹路径：').grid()
Entry(textvariable=tk_path).grid(row=0, column=1)
Button(text='浏览', command = select_dir).grid(row=0, column=2, sticky=EW)

Label(text='新名字：').grid(row=1, column=0)
Entry(textvariable=tk_name).grid(row=1, column=1)

Checkbutton(text='删除旧图', variable=tk_del_old_image, command=tk_del_old_image_save).grid(row=1, column=2, sticky=W)
Checkbutton(text='按日期排序', variable=tk_date_sort, command=tk_date_sort_save).grid(row=2, column=2, sticky=W)
Checkbutton(text='打开文件夹', variable=tk_open_folder, command=tk_open_folder_save).grid(row=3, column=2, sticky=W)

Checkbutton(text='限制图片数量', variable=tk_has_image_num, command=tk_has_image_num_save).grid(row=2, column=0, sticky=W)
Entry(textvariable=tk_image_num).grid(row=2, column=1, sticky=W)

Checkbutton(text='加入尾缀', variable=tk_add_suffix, command=tk_has_image_num_save).grid(row=3, column=0, sticky=W)
Entry(textvariable=tk_suffix).grid(row=3, column=1, sticky=W)

Button(text='打开文件夹', command=open_folder).grid(row=4, column=0, sticky=EW)
Button(text='执行合并', command=run).grid(row=4, column=1, sticky=EW)

# ===============进入消息循环===============
top.mainloop()  #开启菜单