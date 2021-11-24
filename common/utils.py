# C:\Users\zengf\AppData\Local\Programs\Python\Python39 python3
# -*- encoding: utf-8 -*-
# @Author : zeng fanwei
# @File : utils.py
# @Time : 2021/11/23 16:20
# @Software : PyCharm

import json
import logging
import os
from common.userdata import UserData
from common.config import Payload
from concurrent_log_handler import ConcurrentRotatingFileHandler
logger = logging.getLogger(__name__)
formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')
filehandler = ConcurrentRotatingFileHandler(filename="./logs/run.log", maxBytes=5 * 1024 * 1024, backupCount=2, encoding='utf-8')
filehandler.setFormatter(formatter)
logger.setLevel(logging.DEBUG)
logger.addHandler(filehandler)

UidPath = os.path.join(os.path.abspath(os.path.dirname(__file__)).replace("common", "data"), "testUid")
DataPath = os.path.join(os.path.abspath(os.path.dirname(__file__)).replace("common", "data"), "userdata")


# 创建一个新的账号
def create_newid():
    testuid = get_test_uid()
    old = UserData(testuid)
    old.create_new_uid()


# 从本地文件获取uid
def get_test_uid():
    global UidPath
    with open(UidPath, "r") as f:
        return int(f.read())


# 从本地文件获取用户的道具数据信息
def get_prop_data(props):
    global DataPath
    with open(DataPath, "r") as f:
        local_data_json = json.loads(f.read())
        logger.info("local : ", local_data_json)
    result = []
    for k in props:
        if k == "equips":  # 获取装备信息
            if "equipment" in local_data_json:
                result.append([e["equipId"] for e in local_data_json["equipment"]])
            else:
                result.append([])
        if k == "coins":  # 获取用户金币数
            result.append(int(local_data_json["userCurrency"]["coins"]))
        if k == "diamonds":  # 获取用户钻石数
            if "diamonds" in local_data_json["userCurrency"]:
                result.append(int(local_data_json["userCurrency"]["diamonds"]))
            else:
                result.append(0)
        if k == "smallBoxKey":  # 获取小宝箱钥匙数量
            if "smallBoxKey" in local_data_json["userCurrency"].keys():
                result.append(int(local_data_json["userCurrency"]["smallBoxKey"]))
            else:
                result.append(0)
        if k == "largeBoxKey":  # 获取大宝箱钥匙数量
            if "largeBoxKey" in local_data_json["userCurrency"].keys():
                result.append(int(local_data_json["userCurrency"]["largeBoxKey"]))
            else:
                result.append(0)
        if k == "energy":  # 获取用户的体力值
            result.append(int(local_data_json["userLifeValue"]["value"]))
        if k == "items":  # 获取用户的道具数量
            temp = {}
            if "items" in local_data_json:
                for i in local_data_json["items"]:
                    temp[i["itemId"]] = i["count"]
            result.append(temp)
        if k == "exp":  # 获取用户的经验数
            if "exp" in local_data_json["userLevel"]:
                result.append(int(local_data_json["userLevel"]["exp"]))
            else:
                result.append(0)
    logger.info("result : ".format(result))
    return result


# 从本地文件获取用户的transId
def get_transId():
    global DataPath
    with open(DataPath, "r") as f:
        local_data_json = json.loads(f.read())
    if "battleTransId" in local_data_json:
        return int(local_data_json["battleTransId"])
    else:
        return 0


# 修改accesstoken
def change_token():
    global Payload, DataPath
    with open(DataPath, "r") as f:
        local_data_json = json.loads(f.read())
    Payload["commonParams"]["accessToken"] = local_data_json["accessToken"]


if __name__ == '__main__':
    print(get_test_uid())
