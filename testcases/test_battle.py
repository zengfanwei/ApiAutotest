# C:\Users\zengf\AppData\Local\Programs\Python\Python39 python3
# -*- encoding: utf-8 -*-
# @Author : zeng fanwei
# @File : test_battle.py
# @Time : 2021/11/24 10:27
# @Software : PyCharm

import logging
import unittest
from common.utils import get_test_uid, create_newid, get_prop_data, get_transId, change_token
from common.userdata import UserData
from common.punballApi import PunballApi
from concurrent_log_handler import ConcurrentRotatingFileHandler
logger = logging.getLogger(__name__)
formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')
filehandler = ConcurrentRotatingFileHandler(filename="./logs/run.log", maxBytes=5 * 1024 * 1024, backupCount=2, encoding='utf-8')
filehandler.setFormatter(formatter)
logger.setLevel(logging.DEBUG)
logger.addHandler(filehandler)

# 参数
battle_cost = 10
battle_time = 0
level_id = 1005
buy_energy_cost = 100
energy_num = 30
punball = PunballApi()
propdata = []
trans = 0


class TestBattle(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        global trans, propdata, battle_cost, level_id, battle_time, buy_energy_cost, energy_num, punball
        # 创建一个新的账号
        create_newid()
        # 创建新的账号的对象,并登录后台
        user = UserData(get_test_uid())
        user.signin()
        # 修改账号数据
        user.change_data("level", 5)
        user.change_data("diamonds", 501)
        user.change_data("level_id", 1005)
        user.add_prop(1, 1300201, 1)
        # 调用登录接口，记录用户数据
        punball.login()
        change_token()
        props = ["energy", "exp", "coins", "diamonds", "equips", "items"]
        propdata = get_prop_data(props)
        trans = get_transId()

    def test_1_battle_start(self):
        global trans, propdata, battle_cost, level_id, battle_time, buy_energy_cost, energy_num, punball
        trans += 1
        start = punball.battle_start(level_id, trans)
        self.assertEqual(start["code"], 0, msg="接口返回code=0，无异常")
        self.assertTrue(start["commonData"]["updateUserLifeValue"]["isChange"], msg="接口返回用户的体力数据有变化")
        self.assertEqual(start["commonData"]["updateUserLifeValue"]["userLifeValue"]["value"],
                         propdata[0] - battle_cost, msg="接口返回的用户体力数据正确")
        propdata[0] = propdata[0] - battle_cost

    def test_2_battle_end(self):
        global trans, propdata, battle_cost, level_id, battle_time, buy_energy_cost, energy_num, punball
        dto = [{"chapterId": level_id, "chapterLength": 60, "rewards": [{"type": 1, "configId": 1010001, "count": 10},
                {"type": 1, "configId": 1020001, "count": 1000}, {"type": 1, "configId": 1030001, "count": 20},
                {"type": 1, "configId": 1060001, "count": 1}, {"type": 1, "configId": 1060002, "count": 2},
                {"type": 1, "configId": 1060003, "count": 3}, {"type": 1, "configId": 1060004, "count": 4},
                {"type": 1, "configId": 1060005, "count": 5}, {"type": 1, "configId": 1060006, "count": 5},
                {"type": 3, "configId": 3010200, "count": 1}, {"type": 1, "configId": 1070001, "count": 1}],
                "chapterFirstDrop": 2, "transId": trans, "killMonsterCount": 200}]
        end = punball.battle_end(dto, propdata[0], 9999, 2, [])
        self.assertEqual(end["code"], 0, msg="接口返回code=0，无异常")
        self.assertEqual(end["commonData"]["updateUserCurrency"]["userCurrency"]["coins"],
                         propdata[2] + 1000, msg="接口返回的数据中金币数量正确")
        propdata[2] = propdata[2] + 1000
        self.assertEqual(end["commonData"]["updateUserCurrency"]["userCurrency"]["diamonds"],
                         propdata[3] + 20, msg="接口返回的数据中钻石数量正确")
        propdata[3] = propdata[3] + 20
        self.assertEqual(end["commonData"]["updateUserLevel"]["userLevel"]["exp"],
                         propdata[1] + 10, msg="接口返回的数据中经验数量正确")
        propdata[1] = propdata[1] + 10
        self.assertEqual(end["commonData"]["equipment"][0]["equipId"], 3010200, msg="接口返回的数据中获得的装备id正确")
        propdata[4].append(3010200)
        self.assertEqual(end["userChapter"]["chapterId"], level_id + 1, msg="接口返回的数据中账号的关卡id正确")
        level_id += 1
        self.assertEqual(end["battleTransId"], trans, msg="接口返回的数据中transid正确")

    def test_3_buy_energy(self):
        energy = punball.shop_buyenergy(False)
        self.assertEqual(energy[0], energy_num, msg="接口返回用户获得的体力数据正确")
        self.assertEqual(energy[1]["diamonds"], propdata[3] - buy_energy_cost, msg="接口返回的用户钻石数据正确")
        propdata[3] = propdata[3] - buy_energy_cost
        self.assertEqual(energy[2]["value"], propdata[0] + energy_num, msg="接口返回的用户体力数据正确")
        propdata[0] = propdata[0] + energy_num
        self.buy_energy_cost = int(energy[3]["buyLifeValueDiamonds"])


if __name__ == '__main__':
    unittest.main()
