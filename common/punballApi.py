# C:\Users\zengf\AppData\Local\Programs\Python\Python39 python3
# -*- encoding: utf-8 -*-
# @Author : zeng fanwei
# @File : punballApi.py
# @Time : 2021/11/23 14:10
# @Software : PyCharm

import logging
import requests
import json
import os
from concurrent_log_handler import ConcurrentRotatingFileHandler
from common.config import APIurl, APIheaders, Payload
logger = logging.getLogger(__name__)
formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')
filehandler = ConcurrentRotatingFileHandler(filename="./api.log", maxBytes=5 * 1024 * 1024, backupCount=2, encoding='utf-8')
filehandler.setFormatter(formatter)
logger.setLevel(logging.DEBUG)
logger.addHandler(filehandler)


class PunballApi:
    def __init__(self):
        self.userdata_path = os.path.join(os.path.abspath(os.path.dirname(__file__)).replace("common", "data"), "userdata")

    def _post(self, *args, **kwargs):
        logger.info("接口请求参数：{}".format(str(args)+str(kwargs)))
        res = requests.post(*args, **kwargs)
        logger.info("接口返回结果：{}".format(res.text))
        return res

    def login(self):
        logger.info("调用登录接口。")
        temp = Payload
        temp.update({"command": 10101, "platformId": 0, "platformUid2": ""})
        payload = json.dumps(temp)
        res = self._post(APIurl, headers=APIheaders, data=payload)
        resdata = res.json()
        if resdata["code"] != 0:
            raise (Exception("调用登录接口返回失败！"))
        # 将用户每次登录后的最新数据存到本地
        with open(self.userdata_path, "w") as f:
            f.write(json.dumps(resdata))
        return resdata

    def shop_info(self):
        logger.info("调用获取商店信息接口。")
        temp = Payload
        temp.update({"command": 10501})
        payload = json.dumps(temp)
        res = self._post(APIurl, headers=APIheaders, data=payload)
        resdata = res.json()
        if resdata["code"] != 0:
            raise (Exception("调用登录接口返回失败！"))
        return resdata

    def shop_openbox(self, type, cosetype):
        """
        :param type: 宝箱类型  0:单抽, 1:10连抽, 2:小宝箱单抽
        :param cosetype:  消耗资源类型   0广告，1钥匙，2钻石
        :return:  获得的装备列表和玩家的货币数量
        """
        logger.info("调用商店开宝箱接口。")
        temp = Payload
        temp.update({"command": 10503, "type": type, "costType": cosetype})
        payload = json.dumps(temp)
        res = self._post(APIurl, headers=APIheaders, data=payload)
        resdata = res.json()
        if resdata["code"] != 0:
            raise (Exception("调用商店开宝箱接口返回失败！"))
        equips = resdata["commonData"]["equipment"]  # [{rowId: "315",equipId: 3010402,level: 1},]
        currency = {}
        if cosetype == 2 or cosetype == 1:
            currency = resdata["commonData"]["updateUserCurrency"]["userCurrency"]  # {coins: 555757,diamonds: 51500,largeBoxKey: 2}
        return equips, currency

    def shop_buycoin(self, type, isAd):
        """
        :param type: 购买金币类型  1-3对应最少到最多
        :param isAd:  是否是看广告 只有最小档
        :return:  获得的金币数量和玩家的货币数量
        """
        logger.info("调用商店买金币接口。")
        temp = Payload
        temp.update({"command": 10505, "type": type, "isAd": isAd})
        payload = json.dumps(temp)
        res = self._post(APIurl, headers=APIheaders, data=payload)
        resdata = res.json()
        if resdata["code"] != 0:
            raise (Exception("调用商店买金币接口返回失败！"))
        rewards = resdata["commonData"]["reward"]["count"]  # 获得的金币数量
        currency = resdata["commonData"]["updateUserCurrency"]["userCurrency"]  # {coins: 555757,diamonds: 51500,largeBoxKey: 2}
        return rewards, currency

    def shop_buyenergy(self, isAd):
        """
        :param isAd:  是否是看广告
        :return:  获得的体力数量、玩家的货币数量、玩家的体力信息
        """
        logger.info("调用商店买体力接口。")
        temp = Payload
        temp.update({"command": 10507, "isAd": isAd})
        payload = json.dumps(temp)
        print(payload)
        res = self._post(APIurl, headers=APIheaders, data=payload)
        resdata = res.json()
        if resdata["code"] != 0:
            raise (Exception("调用商店买体力接口返回失败！"))
        rewards = resdata["commonData"]["reward"][0]["count"]  # 获得的体力数量
        currency = resdata["commonData"]["updateUserCurrency"]["userCurrency"]  # {coins: 555757,diamonds: 51500,largeBoxKey: 2}
        lifevalue = resdata["commonData"]["updateUserLifeValue"]["userLifeValue"]  # {value: 83,maxValue: 30,lifeTimestamp: "1637654226"}
        return rewards, currency, lifevalue, resdata

    def shop_buydaily(self, position, isAd):
        """
        :param position:  档位 1-3
        :param isAd:  是否是看广告
        :return:   获得的道具数量、玩家的货币数量
        """
        logger.info("调用每日商店购买接口。")
        temp = Payload
        temp.update({"command": 10509, "position": position, "isAd": isAd})
        payload = json.dumps(temp)
        res = self._post(APIurl, headers=APIheaders, data=payload)
        resdata = res.json()
        if resdata["code"] != 0:
            raise (Exception("调用每日商店购买接口返回失败！"))
        rewards = resdata["commonData"]["reward"]  # 获得的奖励以及数量
        currency = resdata["commonData"]["updateUserCurrency"]["userCurrency"]  # {coins: 555757,diamonds: 51500,largeBoxKey: 2}
        return rewards, currency

    def shop_checkgift(self, giftid, index):
        """
        :param giftid:  配置的限时礼包id
        :param index:  第几档
        :return:  礼包购买状态
        """
        logger.info("调用检查礼包是否存在接口。")
        temp = Payload
        temp.update({"command": 10511, "limitGiftPackConfigId": giftid, "index": index})
        payload = json.dumps(temp)
        res = self._post(APIurl, headers=APIheaders, data=payload)
        resdata = res.json()
        if resdata["code"] != 0:
            raise (Exception("调用检查礼包是否存在接口返回失败！"))
        return resdata["state"]  # 礼包购买状态

    def shop_wish(self, equips):
        """
        :param equips:  许愿的装备id列表
        :return:  许愿结果状态
        """
        logger.info("调用许愿池接口。")
        temp = Payload
        temp.update({"command": 10513, "wishEquipIds": equips})
        payload = json.dumps(temp)
        res = self._post(APIurl, headers=APIheaders, data=payload)
        resdata = res.json()
        if resdata["code"] != 0:
            raise (Exception("调用许愿池接口返回失败！"))
        return resdata["wishEquipIds"]  # 许愿池的装备id列表

    def battle_start(self, chapter, trans):
        """
        :param chapter:  章节id
        :param trans:  战斗的transid
        :return:  返回接口返回的数据
        """
        logger.info("调用战斗开始接口。")
        temp = Payload
        temp.update({"command": 10401, "chapterId": chapter, "transId": trans})
        payload = json.dumps(temp)
        res = self._post(APIurl, headers=APIheaders, data=payload)
        resdata = res.json()
        if resdata["code"] != 0:
            raise (Exception("调用战斗开始接口返回失败！"))
        return resdata

    def battle_end(self, dto, life, seconds, cnt, shapters):
        """
        :param dto:  关卡的战斗数据，数据类型：[{"chapterId": 关卡id,
                                            "chapterLength": 关卡长度,
                                            "rewards": 关卡奖励，数据类型[{"type": 1：道具  3：装备,
                                                                        "configId": 道具id,
                                                                        "count":数量}],
                                            "chapterFirstDrop": 1：首次， 2：非首次,
                                            "transId": id,
                                            "killMonsterCount": 杀怪数}]
        :param life:   客户端当前体力数
        :param seconds:  剩余加体力的秒数
        :param cnt:  开始游戏的次数
        :param shapters:  离线开始的章节列表
        :return:
        """
        logger.info("调用战斗结算接口。")
        temp = Payload
        temp.update({"command": 10403, "battleEndDto": dto, "lastLifeValue": life, "lastSeconds": seconds,
                     "startCnt": cnt, "startChapterIds": shapters})
        payload = json.dumps(temp)
        res = self._post(APIurl, headers=APIheaders, data=payload)
        resdata = res.json()
        if resdata["code"] != 0:
            raise (Exception("调用战斗结算接口返回失败！"))
        return resdata


if __name__ == '__main__':
    ap = PunballApi()
    print(ap.login())
    # print(ap.shop_info())