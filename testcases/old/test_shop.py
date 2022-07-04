# C:\Users\zengf\AppData\Local\Programs\Python\Python39 python3
# -*- encoding: utf-8 -*-
# @Author : zeng fanwei
# @File : test_shop_info.py
# @Time : 2021/11/23 16:32
# @Software : PyCharm

import unittest
import requests
from common.utils import get_test_uid, create_newid, get_prop_data
from common.userdata import UserData
from common.punballApi import PunballApi


class TestShop(unittest.TestCase):
    def setUp(self) -> None:
        # 创建一个新的账号
        create_newid()
        # 创建新的账号的对象,并登录后台
        self.user = UserData(get_test_uid())
        self.user.signin()
        # 修改账号数据
        self.user.change_data("level", 5)
        self.user.change_data("level_id", 1005)
        self.user.add_prop(1, 1300201, 1)
        # 调用登录接口，记录用户数据
        self.punball = PunballApi()
        props = ["equips", "coins", "diamonds", "smallBoxKey", "largeBoxKey"]
        propdata = get_prop_data(props)

    def test_get_info(self):
        shop = self.punball.shop_info()
        self.assertEqual(shop["code"], 0, msg="接口返回code=0，无异常")
        self.assertIn("dailyStores", shop.keys(), msg="接口返回的数据中包含dailyStores")
        self.assertIn("shopChapterGifts", shop.keys(), msg="接口返回的数据中包含shopChapterGifts")
        self.assertIn("wishEquipIds", shop.keys(), msg="接口返回的数据中包含wishEquipIds")

    def test_open_box(self):
        shop = self.punball.shop_openbox(0, 0)
        self.assertEqual(shop["code"], 0, msg="接口返回code=0，无异常")
        self.assertIn("dailyStores", shop.keys(), msg="接口返回的数据中包含dailyStores")
        self.assertIn("shopChapterGifts", shop.keys(), msg="接口返回的数据中包含shopChapterGifts")
        self.assertIn("wishEquipIds", shop.keys(), msg="接口返回的数据中包含wishEquipIds")


if __name__ == '__main__':
    unittest.main()
