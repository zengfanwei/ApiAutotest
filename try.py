# C:\Users\zengf\AppData\Local\Programs\Python\Python39 python3
# -*- encoding: utf-8 -*-
# @Author : zeng fanwei
# @File : try.py
# @Time : 2021/11/22 11:45
# @Software : PyCharm

# import requests
#
#
# def print_hi():
#     data = {"command": 10101,
#             "commonParams": {
#                  "platformUid": "a_2375628593256291647",
#                  "version": 12,
#                  "deviceId": "9e1031012d3607b6e9028c4948668511",
#                  "accessToken": "OGTpYbec1vP1BYi9YKqV2fPqxfgdsWAN92+Syv315ShC3CeK/vyLc1Et6fcCVOKw+q7t4uqkWC7WAm2ogTXLNg=="},
#              "platformId": 0,
#              "platformUid2": "",
#              "secret": "acc2eadf31b2729a26efa8589a5dceb4"}
#     url = "https://test-punball-v2.habby.com/internal"
#     res = requests.post(url, data=data)
#     print(res.status_code)
#     print(res.content)
#     print(res.text)
#     print(res.url)
#
#
# if __name__ == '__main__':
#     print_hi()
# import requests
#
# url = "https://wiki-punball.habby.com/login?serverIdx=0&userId=10618502"
#
# payload = ""
# headers = {
#   'Cookie': 'connect.sid=s%3A_inqfASn_5Ej__nFWVBr0jWVth4YgW4l.h8aPQi8%2BTsZWoOy3HUTDQsOxuABCc4Q1suDgTF95umw'
# }
#
# response = requests.request("GET", url, headers=headers, data=payload)
#
# print(response.text)

from common.utils import create_newid, get_test_uid, get_prop_data, change_token
from common.userdata import UserData
from common.punballApi import PunballApi

create_newid()
# 创建新的账号的对象,并登录后台
user = UserData(get_test_uid())
user.signin()
user.change_data("level", 5)
user.change_data("level_id", 1005)
user.add_prop(1, 1300201, 1)
punball = PunballApi()
punball.login()
change_token()
props = ["energy", "exp", "coins", "diamonds", "equips", "items"]
propdata = get_prop_data(props)
print(propdata)
buy = punball.shop_buyenergy(False)
print(buy)