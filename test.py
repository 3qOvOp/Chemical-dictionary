import os
import re
import chardet
import aliyunCR

class GetName():

    '''
    获取图片名称
    '''

    def __init__(self,path,save_path):
        # 存放图片的文件夹路径
        self.path = path
        self.save_path = save_path
    def get_name(self):
        filelist = os.listdir(self.path)

        appCode = '32d3037c91ff4c4d88e2da457fb48e92'
        # path = 'E:\BDH\Data\sources\CLDCD\imgContext/'
        for item in filelist:
            print(len(item))
            page_text = aliyunCR.aliyunCR(appCode=appCode,img_src=path+item)
            txt_name = re.findall('(.*).jpg',item)[0]
            with open(self.save_path+txt_name+'.txt','w',encoding='utf-8') as f:
                f.write(page_text)

            # with open('E:\BDH\Data\sources\CLDCD\OCRJson/' + txt_name + '.txt', 'rb') as f:
            #     data = f.read()
            # type = chardet.detect(data)
            # result = data.decode(type["encoding"])
            #
            # print(result)

    def get_name2(self):
        appCode = '32d3037c91ff4c4d88e2da457fb48e92'
        for dir in os.listdir(self.path):
            ab_dir = os.path.join(self.path, dir)
            for item in os.listdir(ab_dir):
                print(len(item))
                page_text = aliyunCR.aliyunCR(appCode=appCode, img_src=os.path.join(ab_dir, item))
                txt_name = re.findall('(.*).jpg', item)[0]
                # mkd = os.path.join(save_path,dir)
                # os.mkdir(mkd)
                with open(os.path.join(save_path,txt_name + '.txt') , 'w', encoding='utf-8') as f:
                    f.write(page_text)

if __name__ == '__main__':
    try:
        save_path = 'OCRresult/'
        path = 'images/'
        get_name = GetName(path,save_path)
        get_name.get_name2()

    except Exception as e :
        print(e)

