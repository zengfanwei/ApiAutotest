# C:\Users\zengf\AppData\Local\Programs\Python\Python39 python3
# -*- encoding: utf-8 -*-
# @Author : zeng fanwei
# @File : userdata.py
# @Time : 2021/11/23 10:29
# @Software : PyCharm

import logging
import requests
import os
import json
from concurrent_log_handler import ConcurrentRotatingFileHandler
from common.config import Headers, SignInUrl, ChangeUrl, DoType
from common.punballApi import PunballApi
logger = logging.getLogger(__name__)
formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')
filehandler = ConcurrentRotatingFileHandler(filename="./userdata.log", maxBytes=5 * 1024 * 1024, backupCount=2, encoding='utf-8')
filehandler.setFormatter(formatter)
logger.setLevel(logging.DEBUG)
logger.addHandler(filehandler)


class UserData:
    def __init__(self, gameuid):
        self.gameuid = str(gameuid)
        self.userdata_path = os.path.join(os.path.abspath(os.path.dirname(__file__)).replace("common", "data"), "testUid")
        print(self.userdata_path)

    def _request(self, *args, **kwargs):
        logger.info("接口请求参数：{}".format(str(args)+str(kwargs)))
        res = requests.request(*args, **kwargs)
        logger.info("接口返回结果：{}".format(res.text))
        return res

    def signin(self):
        logger.info("登录服务后台。")
        url = SignInUrl.replace("9999999", self.gameuid)
        print(url)
        res = self._request("GET", url, data="", headers=Headers)
        resdata = res.json()
        if resdata["code"] != 0:
            raise (Exception("登录弹球后台工具失败！"))
        return resdata

    def change_data(self, module, num):  # 通用修改数据的方法，不包括发道具、重置分享领取记录、
        logger.info("修改账号数据，{}".format(module))
        url = ChangeUrl.replace("xxx", DoType[module]).replace("999", str(num))
        res = self._request("GET", url, data="", headers=Headers)
        resdata = res.json()
        if resdata["code"] != 0:
            raise (Exception("修改账号数据失败！"))
        return res

    def add_prop(self, num, itemid, level):  # 添加道具
        logger.info("给账号添加道具，{}".format(str(itemid)))
        url = "https://wiki-punball.habby.com/addResource?serverIdx=0&resType=3&" \
              "resNum={0}&itemId={1}&otherData={2}".format(str(num), str(itemid), str(level))
        res = self._request("GET", url, data="", headers=Headers)
        resdata = res.json()
        if resdata["code"] != 0:
            raise (Exception("给账号添加道具失败！"))
        return res

    def delete_account(self):  # 删除账号
        logger.info("删除此账号，{}".format(self.gameuid))
        url = "https://wiki-punball.habby.com/addResource?serverIdx=0&resType=22&resNum=1&itemId=1040031&otherData=1"
        res = self._request("GET", url, data="", headers=Headers)
        resdata = res.json()
        if resdata["code"] != 0:
            raise (Exception("删除账号失败！"))
        open(self.userdata_path, 'w').close()
        return res

    def create_new_uid(self):
        self.delete_account()
        punball = PunballApi()
        newdate = punball.login()
        uid = newdate["userId"]
        with open(self.userdata_path, "w") as f:
            f.write(uid)


if __name__ == '__main__':
    user = UserData(90000138)
    print(user.signin())
    user.create_new_uid()