import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
import webbrowser as web
import sys
import os

import config


cf = config.Config('', 1, './')


def check_menu():
    web.open('https://github.com/745692208/ImageMergeTool')


def select_files():
    files = filedialog.askopenfilenames()
    print(files)


def browse():
    print('browse')
    dir = os.path.normpath(filedialog.askdirectory())
    if dir != '.':
        cf.save('base', 'path', dir)


def open_folder(self):
    try:
        os.startfile(self.entry_path.get())
    except Exception:
        messagebox.showerror("错误", "请输入正确的文件夹路径！")


def changeTab():
    index = tab_index.get()
    cf.save('base', 'tab_index', str(index))
    lf_option.pack_forget()
    for ftab in ftab_list:
        ftab.pack_forget()
    ftab_list[index].pack(fill='x')
    lf_option.pack(side='top', fill='x')


# GUI初始化
app = tk.Tk()
app.title('图片合并工具 1.0.0')
# app.geometry('400x200')
menubar = tk.Menu(app)
menubar.add_command(label='关于', command=check_menu)
app['menu'] = menubar

# 1 第0行 标签容器 创建标签

fTab = tk.Frame(app)
fTab.pack(side='top', fill='x')
tab_index = tk.IntVar()
tab_index.set(cf.load('base', 'tab_index', 0))

for i, name in enumerate(['选择图片', '选择文件夹']):
    ttk.Radiobutton(
        fTab, text=name, value=i,
        variable=tab_index, command=changeTab)\
        .pack(side='left')

# 第一行 内容
ftab_list = []
# 选择文件
lf_select = ttk.LabelFrame(app, text='Select Image')
lf_select.pack(side='top', fill='x')
ftab_list.append(lf_select)
tk.Label(lf_select, text='已选择5个文件', anchor='w')\
    .pack(side='left', fill='x', expand=1)
ttk.Button(lf_select, text='选择文件', command=select_files).pack(side='left')
# 路径
lf_path = ttk.LabelFrame(app, text='Path')
lf_path.pack(side='top', fill='x')
ftab_list.append(lf_path)
tk.Label(lf_path, text='文件夹路径：').pack(side='left')
ttk.Entry(lf_path, ).pack(side='left', fill='x', expand=1)
ttk.Button(lf_path, text='浏览', command=browse).pack(side='left')

# 第二行 选项
lf_option = ttk.LabelFrame(app, text='Option')
lf_option.pack(side='top', fill='x')

f_name = ttk.Frame(lf_option)
f_name.pack(side='top', fill='x')
tk.Label(f_name, text='Name：').pack(side='left')
ttk.Entry(f_name, ).pack(side='left')
ttk.Checkbutton(f_name, text='添加日期').pack(side='left')

lf_cb = tk.Frame(lf_option)
lf_cb.pack(side='top', fill='x')
ttk.Checkbutton(lf_cb, text='删除旧文件').pack(side='left')
ttk.Checkbutton(lf_cb, text='创建New文件夹').pack(side='left')
ttk.Checkbutton(lf_cb, text='完成后打开文件夹').pack(side='left')

lf_button = tk.Frame(lf_option)
lf_button.pack(side='top', fill='x')
ttk.Button(lf_button, text='合并').pack(side='top', fill='both', expand=1)

# run
changeTab()
app.mainloop()
app.quit()
sys.exit()
