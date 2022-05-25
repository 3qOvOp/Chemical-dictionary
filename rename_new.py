import os
import re


def get_filelist(dirs):
    # 对于总文件夹（images）
    for dir in os.listdir(dirs):
        # 文件夹第一个数字为该文件夹下文件开始页码
        page_start_num = int(re.findall("(\d+)-", dir)[0])
        # 文件绝对目录
        ab_dir = os.path.join(dirs, dir)
        print(ab_dir)
        # 对于每子目录（1-34）
        num = 0
        for file in os.listdir(ab_dir):
            # print("file",file)
            # i：第1页和17页为单页，其余为双页
            # num:page_num = page_start_num + 2*um - 3(观察所得)
            # 重命名：页面页码恰好=起始页码+2*图片文件下索引-3
            # （除了第一页，当第一页改为第1.5页时符合该规则）

            src = os.path.join(ab_dir, file)
            page_num = int(page_start_num +  num )

            dst = os.path.join(ab_dir, 'HXHGDCD-P' + str(page_num) +
                                '.jpg')
            os.rename(src, dst)


if __name__ == "__main__":
    get_filelist('E:/pythonProject/untitled/venv/images')