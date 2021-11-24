# C:\Users\zengf\AppData\Local\Programs\Python\Python39 python3
# -*- encoding: utf-8 -*-
# @Author : zeng fanwei
# @File : config.py
# @Time : 2021/11/23 11:13
# @Software : PyCharm

APIurl = "https://test-punball-v2.habby.com/internal"
SignInUrl = "https://wiki-punball.habby.com/login?serverIdx=0&userId=9999999"
ChangeUrl = "https://wiki-punball.habby.com/addResource?serverIdx=0&resType=xxx&resNum=999&itemId=1010001&otherData=999"
APIheaders = {
  'Content-Type': 'application/json'
}
Headers = {
  'Cookie': 'connect.sid=s%3A_inqfASn_5Ej__nFWVBr0jWVth4YgW4l.h8aPQi8%2BTsZWoOy3HUTDQsOxuABCc4Q1suDgTF95umw'
}
DoType = {"coin": "1", "diamonds": "2", "energy": "30", "level": "19", "exp": "25", "mask": "13", "level_id": "4",
          "level_length": "29", "last_login": "33", "login_days": "75", "money": "88", "big_chest": "34",
          "small_chest": "39", "reset_talent": "41", "small_talent": "72", "big_talent": "73", "reset_dailyshop": "36",
          "reset_share": "74", "dailyshop_refresh": "84", "reset_level_chest": "38", "reset_ad": "52",
          "buy_energy_time": "71", "reset_energy_buy": "76", "clear_equipment": "59", "clear_scroll": "80"}

Payload = {"commonParams":
               {"platformUid": "a_2375628593256291647",
                "version": 12,
                "deviceId": "9e1031012d3607b6e9028c4948668511",
                "accessToken": "a3lwS6u4WIOEfQLGj+i1FaT7oH/JSRj3/P3cZYejjvhC3CeK/vyLc1Et6fcCVOKw+q7t4uqkWC7WAm2ogTXLNg=="},
            "secret": "acc2eadf31b2729a26efa8589a5dceb4"}