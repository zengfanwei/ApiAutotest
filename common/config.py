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
  'Cookie': 'connect.sid=s%3ATqcWzY0Uj7A7z-T_FKOTHBMsQ5j4G2A4.vcV3nkouF39%2FEblY%2BTsUsMoQVQueHpOqixDVB2HDzu4'
}
DoType = {"coin": "1", "diamonds": "2", "energy": "30", "level": "19", "exp": "25", "mask": "13", "level_id": "4",
          "level_length": "29", "last_login": "33", "login_days": "75", "money": "88", "big_chest": "34",
          "small_chest": "39", "reset_talent": "41", "small_talent": "72", "big_talent": "73", "reset_dailyshop": "36",
          "reset_share": "74", "dailyshop_refresh": "84", "reset_level_chest": "38", "reset_ad": "52",
          "buy_energy_time": "71", "reset_energy_buy": "76", "clear_equipment": "59", "clear_scroll": "80"}

Payload = {"commonParams":
               {"platformUid": "",
                "version": 14,
                "deviceId": "HabbyNewDevice001",
                "accessToken": ""},
            "secret": "acc2eadf31b2729a26efa8589a5dceb4"}