import PIL.Image as Image
import os
import time
from tkinter import messagebox


class Core:
    def image_merge(self, path, name, bIsAddSuffix, suffix, bIsHasNum,
                    images_num, bIsOpenFold, bIsRemoveOldImage, bIsDateSort):
        '''
        :parma path, str, 需要合并图片的所在路径；
        :parma name, str, 合并后文件的名字；
        :parma bIsAddSuffix, bool, 是否添加尾缀；
        :parma suffix, str, 尾缀；
        :parma bIsHasNum, bool, 是否有图片数量限制；
        :parma images_num, str, 限制的图片数量；
        :parma bIsOpenFold, bool, 是否完成后打开文件夹；
        :parma bIsRemoveOldImage, bool, 是否完成后删除合并前的图片；
        :parma bIsDateSort, bool, 是否按日期排序图片进行合并；
        '''
        print("开始")
        image_format = ['.png', '.PNG', '.jpg', '.JPG']
        path = path + '/'

        # 获取图片并判断名字和数量
        try:
            image_names = [
                name for name in os.listdir(path)
                for item in image_format if os.path.splitext(name)[1] == item
            ]
        except Exception():
            print("没有找到文件夹")
            messagebox.showerror("错误", "请输入正确的文件夹路径")
            return
        image_num = len(image_names)

        if bIsDateSort:
            image_names = sorted(
                image_names,
                key=lambda x: os.path.getmtime(os.path.join(path, x)))

        if bIsHasNum:
            try:
                if image_num > int(images_num):
                    image_num = int(images_num)
                    image_names = image_names[
                        len(image_names) - image_num:len(image_names)]
            except Exception:
                messagebox.showerror("错误", "请输入正确的限制数量")
                return

        # 获取第一张图片的大小
        image_size = Image.open(path + image_names[0]).size

        # 创建与合并图片， 参考：https://www.cnblogs.com/gisoracle/p/12081967.html
        new_image = Image.new(
            'RGB', (image_size[0] * image_num, image_size[1]))  # 创建一个新图
        for i in range(0, image_num):
            image_obj = Image.open(path + image_names[i])
            new_image.paste(image_obj, (i * image_size[0], 0))

        # 创建目录
        if os.path.exists(path + "new") == 0:
            os.mkdir(path + "new")
        # 保存图片
        time_date = time.strftime("%y-%m-%d")
        if bIsAddSuffix:
            new_image.save(
                r'{}new\{}_{}_{}.png'.format(path, name, time_date, suffix))
        else:
            new_image.save(
                r'{}new\{}_{}.png'.format(path, name, time_date))
        # 打开文件夹
        if bIsOpenFold:
            os.startfile(path + "new/")
        # 删除旧文件
        if bIsRemoveOldImage:
            for i in image_names:
                os.remove(path + i)
        print("执行完成!")


if __name__ == '__main__':
    core = Core()
    core.image_merge(
        r'E:\Python\down\《星云》',
        'name',
        1,
        'suffix',
        1,
        'asd',
        1,
        0,
        0
    )
