######################################
#    脚本作者: NothAmor               #
# 作者博客: https://www.nothamor.cn   #
######################################

import requests
import random
import json
import time

def login(phoneNumber, password):
    # 设置登录链接, 登陆请求头, 登陆体
    loginUrl = "https://api.moguding.net:9000/session/user/v1/login"

    loginHeaders = {
        'Accept-Language':"zh-CN,zh;q=0.8",
        'roleKey': 'student',
        'Host':'api.moguding.net:9000',
        "Content-Type": "application/json; charset=UTF-8",
        "Cache-Control": "no-cache",
        'User-Agent': "Mozilla/5.0 (Linux; Android 5.1.1; MI 9 Build/LMY48Z; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36 wxhappwebview/1.1"
    }

    loginForm = {
        "phone": phoneNumber,
        "password": password,
        "loginType": "android",
        "uuid": ""
    }

    while True:
        # 登陆请求
        loginResponse = requests.post(url=loginUrl, headers=loginHeaders, data=json.dumps(loginForm))
        if loginResponse.status_code != 200:
            continue
        else:
            break

    auth = json.loads(loginResponse.text)
    token = auth["data"]["token"]
    userId = auth["data"]["userId"]

    print("登陆成功")

    return token, userId

def healthyCheck(token, form):
    healthyCheckUrl = "https://api.moguding.net:9000/practice/hlj/health/reports/v1/save"
    healthyCheckHeader = {
        'User-Agent': "Mozilla/5.0 (Linux; Android 5.1.1; MI 9 Build/LMY48Z; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36 wxhappwebview/1.1",
        "Accept": "application/json, text/plain, */*",
        "Authorization": token,
        "Content-Type": "application/json;charset=UTF-8",
        "Referer": "https://api.moguding.net:10000/",
        "Accept-Language": "zh-CN,en-US;q=0.8",
        "X-Requested-With": "com.smilingmobile.practice",
        "Origin": "https://api.moguding.net:10000"
    }
    healthyCheckForm = {
        "practiceType": "",
        "isAuto": 1,
        "companyName": "",
        "companyType": "",
        "companyTypeValue": "",
        "state": 1,
        "isolationAddress": "", # 好像是隔离地址
        "otherDesc": "",
        "healthReportsId": "",
        "temperature": "36.7" # 体温
    }

    checkForm = {}
    checkForm.update(healthyCheckForm)
    checkForm.update(form)
    print("开始打卡")

    while True:
        healthyCheckResponse = requests.post(url=healthyCheckUrl, headers=healthyCheckHeader, data=json.dumps(checkForm))
        if healthyCheckResponse.status_code != 200:
            continue
        else:
            break

    return healthyCheckResponse.text


if __name__ == "__main__":
    print("程序开始运行")

    # 参数说明
    # 多账户就在列表中新增字典

    # phoneNumber是 蘑菇钉/工学云 的登陆账号
    # password是登录密码
    
    # sendKey是server酱的发送秘钥
    # province是省份
    # city是城市
    # area是区
    # address是详细地址
    # isVaccines是是否接种新冠疫苗, 是为1, 不是为0
    # lifeState是健康状况, 健康为4
    # 是否为高风险地区, 否为0, 是为1
    accounts = {
        "account": [
            {
                "phoneNumber": "",
                "password": "",
                "sendKey": "",
                "checkForm": {
                    "province": "",
                    "city": "",
                    "area": "",
                    "address": "",
                    "isVaccines": 1,
                    "lifeState": 4,
                    "isHighRiskArea": 0
                }
            },
        ]
    }

    time.sleep(random.randint(1, 30))
    for account in accounts["account"]:
        randomDelay = random.randint(1, 120)

        accountStorage = {
            "token": "",
            "userId": ""
        }

        # 填写账号密码
        phoneNumber = account["phoneNumber"]
        password = account["password"]

        print("正在打卡账户为: {}".format(phoneNumber))

        # server酱秘钥
        sendKey = account["sendKey"]

        account["token"], account["userId"] = login(phoneNumber, password)

        msg = json.loads(healthyCheck(account["token"], account["checkForm"]))

        if msg["msg"] == "success" and msg["code"] == 200:
            print("打卡成功!")
            if account["sendKey"] != "":
                checkResultResponse = requests.get("https://sctapi.ftqq.com/{key}.send?title=工学云健康打卡成功!&desp=打卡状态码: {resultCode}, 打卡返回信息: {resultMsg}".format(key=sendKey, resultCode=msg["code"], resultMsg=msg["msg"]))
        else:
            print("打卡失败!")
            if account["sendKey"] != "":
                checkResultResponse = requests.get("https://sctapi.ftqq.com/{key}.send?title=工学云健康打卡失败!&desp=打卡状态码: {resultCode}, 打卡返回信息: {resultMsg}".format(key=sendKey, resultCode=msg["code"], resultMsg=msg["msg"]))
        
        print("{}秒后进行下一个任务".format(randomDelay))
        time.sleep(randomDelay)

