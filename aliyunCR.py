import urllib.request
import urllib.parse
import json
import time
import base64
import docx
import re
import csv
from docx import Document


def aliyunCR(appCode, img_src):
    with open(img_src, 'rb') as f:  # 以二进制读取本地图片
        data = f.read()
        encodestr = str(base64.b64encode(data), 'utf-8')
    # 请求头
    # 请修改为你自己的appcode，可从云市场订单或者api网关处获得
    AppCode = appCode
    headers = {
        'Authorization': 'APPCODE ' + AppCode,
        'Content-Type': 'application/json; charset=UTF-8'
    }

    def posturl(url, data={}):
        params = json.dumps(dict).encode(encoding='UTF8')
        req = urllib.request.Request(url, params, headers)
        r = urllib.request.urlopen(req)
        html = r.read()
        r.close();
        return html.decode("utf8")

    # def posturl(url, data={}):
    #     try:
    #         params = json.dumps(dict).encode(encoding='UTF8')
    #         req = urllib.request.Request(url, params, headers)
    #         r = urllib.request.urlopen(req)
    #         html = r.read()
    #         r.close();
    #         return html.decode("utf8")
    #     except urllib.error.HTTPError as e:
    #         print(e.code)
    #         print(e.read().decode("utf8"))
        time.sleep(1)

    url_request = "https://ocrapi-advanced.taobao.com/ocrservice/advanced"
    dict = {'img': encodestr}

    page_text = posturl(url_request, data=dict)
    return page_text