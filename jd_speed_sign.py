# 京东极速版签到+赚现金任务
# 每日9毛左右，满3，10，50可兑换无门槛红包
# ⚠️⚠️⚠️一个号需要运行20多分钟左右
# 活动时间：长期
# 活动入口：京东极速版app-现金签到
# 已支持IOS双京东账号,Node.js支持N个京东账号
# 脚本兼容: QuantumultX, Surge, Loon, JSBox, Node.js
# ========Quantumultx==========
# [task_local]
# #京东极速版
# 15 2,14 * * * jd_speed_sign.js,
# ===========Loon==========
# [Script]
# cron "15 2,14 * * *" script-path=jd_speed_sign.js,tag=京东极速版
# ==========Surge============
# 京东极速版 = type=cron,cronexp="15 2,14 * * *",wake-system=1,timeout=33600,script-path=jd_speed_sign.js
# ========小火箭======
# 京东极速版 = type=cron,script-path=jd_speed_sign.js, cronexpr="15 2,14 * * *", timeout=33600, enable=True
import calendar
import datetime
import json
import logging
import random
import re
import time

import requests
import user
from util.url_utils import task_url
from util.url_utils import task_get_url

# import sendNotify

# notify = sendNotify
# Node.js用户请在jdCookie.js处填写京东ck;
# jdCookieNode = require('./jdCookie.js') : ''
jdCookieNode = ''
cookiesArr = []
cookie = ''
message = ''
IPError = False  # 403 ip黑
# if (user_info.isNode()) {
#   Object.keys(jdCookieNode).forEach((item) => {
#     cookiesArr.push(jdCookieNode[item])
#   })
#   if (process.env.JD_DEBUG & process.env.JD_DEBUG == 'False') print = () => {
#   };
# else:
#   cookiesArr = [user_info.getdata('CookieJD'), user_info.getdata('CookieJD2'), ...jsonParse(user_info.getdata('CookiesJD') || "[]").map(item => item.cookie)].filter(item => !!item);
# }
JD_API_HOST = 'https://api.m.jd.com/'
actCode = 'visa-card-001'

user_info = user.UserInfo()

date = datetime.datetime.now().date()
week_day, month_count_day = calendar.monthrange(date.year, date.month)
last_month_day = datetime.date(date.year, date.month, day=month_count_day)
user_info.last_day = last_month_day == date

def safe_get(content):
    try:
        if len(content) > 0:
            return True
    except Exception as e:
        logging.exception(e)
        print('京东服务器访问数据为空，请检查自身设备网络情况')
        return False


def jd_global():
    try:
        rich_man_index()
        wheels_home()
        ap_task_ist()
        wheels_home()

        sign_init()
        sign()
        invite()
        invite2()
        score = 0
        total = 0
        task_list()
        query_joy()
        sign_init()
        cash()
        if last_month_day:
            print('月底了,自动领下单红包奖励')
            order_reward()
        show_msg()
    except Exception as e:
        logging.exception(e)


def show_msg():
    locale_message = f'本次运行获得{user_info.score}金币，共计{user_info.total}金币\n可兑换 {round(user_info.total / 10000, 2)} 元京东红包\n兑换入口：京东极速版->我的->金币'
    print(user_info.name, '', f'京东账号{user_info.index}{user_info.nickName}\n{locale_message}')


def sign_init():
    url_str, headers = task_url('speedSignInit', {
        "activityId": "8a8fabf3cccb417f8e691b6774938bc2",
        "kernelPlatform": "RN",
        "inviterId": "U44jAghdpW58FKgfqPdotA=="
    }, cookie)
    resp = requests.get(url=url_str, headers=headers)
    print("result", resp.content.decode("utf-8"))
    try:
        # if err:
        # print(f'{json.dumps(err)}')
        # print(f'{user_info.name} API请求失败，请检查网路重试')
        # else:
        data = json.loads(resp.content)
        print(data)
    except Exception as e:
        logging.exception(e)


def sign():
    url_str, headers = task_url('speedSign', {
        "kernelPlatform": "RN",
        "activityId": "8a8fabf3cccb417f8e691b6774938bc2",
        "noWaitPrize": "False"
    }, cookie)
    resp = requests.get(url=url_str, headers=headers)
    print("result", resp.content.decode("utf-8"))
    try:
        if safe_get(resp.content):
            data = json.loads(resp.content)
            if data['subCode'] == 0:
                print(f'签到获得{data["data"]["signAmount"]}现金，共计获得{data["data"]["cashDrawAmount"]}')
            else:
                print(f'签到失败，{data["msg"]}')
    except Exception as e:
        logging.exception(e)


def task_list():
    url_str, headers = task_url('ClientHandleService.execute', {
        "version": "3.1.0",
        "method": "newTaskCenterPage",
        "data": {
            "channel": 1
        }
    }, cookie)
    resp = requests.get(url=url_str, headers=headers)
    print("result", resp.content.decode("utf-8"))
    try:
        if safe_get(resp.content):
            data = json.loads(resp.content)
            for task in data['data']:
                user_info.taskName = task['taskInfo']['mainTitle']
                if task['taskInfo']['status'] == 0:
                    if task['taskType'] >= 1000:
                        do_task(task['taskType'])
                        time.sleep(1)
                    else:
                        user_info.canStartNewItem = True
                        while user_info.canStartNewItem:
                            if task.taskType != 3:
                                query_item(task.taskType)
                            else:
                                start_item("", task.taskType)
                else:
                    print(f'{user_info.taskName}已完成')
                if IPError:
                    logging.error('API请求失败，停止执行')
                    break
    except Exception as e:
        logging.exception(e)


def do_task(task_id):
    url_str, headers = task_url('ClientHandleService.execute', {
        "method": "marketTaskRewardPayment",
        "data": {
            "channel": 1,
            "clientTime": int(time.time() * 1000) + 0.588,
            "activeType": task_id
        }
    }, cookie)
    resp = requests.get(url=url_str, headers=headers)
    print("result", resp.content.decode("utf-8"))
    try:
        if safe_get(resp.content):
            data = json.loads(resp.content)
            if data.code == 0:
                print(f'{data["data"]["taskInfo"]["mainTitle"]}任务完成成功，预计获得${data["data"]["reward"]}金币')
            else:
                print(f'任务完成失败，{data["message"]}')
    except Exception as e:
        logging.exception(e)


def query_joy():
    url_str, headers = task_url('ClientHandleService.execute', {"method": "queryJoyPage", "data": {"channel": 1}}, cookie)
    resp = requests.get(url=url_str, headers=headers)
    print("resp = ", resp.content.decode("utf-8"))
    try:
        if safe_get(resp.content):
            data = json.loads(resp.content)
            if 'taskBubbles' in data['data']:
                for task in data['data']['taskBubbles']:
                    reward_task(task['id'], task['activeType'])
                    user_info.wait(500)
    except Exception as e:
        logging.exception(e)


def reward_task(task_id, active_type):
    url_str, headers = task_url('ClientHandleService.execute', {
        "method": "joyTaskReward",
        "data": {
            "id": task_id,
            "channel": 1,
            "clientTime": int(time.time() * 1000) + 0.588,
            "activeType": active_type
        }
    }, cookie)
    resp = requests.get(url=url_str, headers=headers)
    print("resp = ", resp.content.decode("utf-8"))
    try:
        if safe_get(resp.content):
            data = json.loads(resp.content)
            if data.code == 0:
                user_info.score += data.data.reward
                print(f'气泡收取成功，获得${data.data.reward}金币')
            else:
                print(f'气泡收取失败，{data.message}')
    except Exception as e:
        logging.exception(e)


def query_item(active_type=1):
    url_str, headers = task_url('ClientHandleService.execute', {
        "method": "queryNextTask",
        "data": {
            "channel": 1,
            "activeType": active_type
        }
    }, cookie)
    resp = requests.get(url=url_str, headers=headers)
    print("resp = ", resp.content.decode("utf-8"))
    try:
        if safe_get(resp.content):
            data = json.loads(resp.content)
            if data.code == 0 & data.data:
                start_item(data.data.nextResource, active_type)
            else:
                print(f'商品任务开启失败，{data.message}')
                user_info.canStartNewItem = False
                IPError = True
    except Exception as e:
        logging.exception(e)


def start_item(active_id, active_type):
    url_str, headers = task_url('ClientHandleService.execute', {
        "method": "enterAndLeave",
        "data": {
            "activeId": active_id,
            "clientTime": int(time.time() * 1000),
            "channel": "1",
            "messageType": "1",
            "activeType": active_type,
        }
    }, cookie)
    resp = requests.get(url=url_str, headers=headers)
    print("resp = ", resp.content.decode("utf-8"))
    try:
        if safe_get(resp.content):
            data = json.loads(resp.content);
            if data.code == 0 & data.data:
                if data.data.taskInfo.isTaskLimit == 0:
                    param = data.data.taskInfo
                    if active_type != 3:
                        param["videoBrowsing"] = 5 if active_type == 1 else 10
                    print(
                        f'【{param["taskCompletionProgress"] + 1}/{param["taskCompletionLimit"]}】浏览商品任务记录成功，等待{param["videoBrowsing"]}秒')
                    user_info.wait(param["videoBrowsing"] * 1000)
                    end_item(data.data.uuid, active_type, active_id, param["videoBrowsing"] if active_type == 3 else "")
                else:
                    print(f'{user_info.taskName}任务已达上限')
                    user_info.canStartNewItem = False
            else:
                user_info.canStartNewItem = False
                print(f'{user_info.taskName}任务开启失败，{data.message}')
    except Exception as e:
        logging.exception(e)


def end_item(uuid, active_type, active_id="", video_time_length=""):
    url_str, headers = task_url('ClientHandleService.execute', {
         "method": "enterAndLeave",
         "data": {
             "channel": "1",
             "clientTime": int(time.time() * 1000),
             "uuid": uuid,
             "videoTimeLength": video_time_length,
             "messageType": "2",
             "activeType": active_type,
             "activeId": active_id
         }
     }, cookie)
    resp = requests.get(url=url_str, headers=headers)
    print("resp = ", resp.content.decode("utf-8"))
    try:
        if safe_get(resp.content):
            data = json.loads(resp.content)
            if data.code == 0 & data.isSuccess:
                reward_item(uuid, active_type, active_id, video_time_length)
            else:
                print(f'{user_info.taskName}任务结束失败，{data.message}')
    except Exception as e:
        logging.exception(e)


def reward_item(uuid, active_type, active_id="", video_time_length=""):
    url_str, headers = task_url('ClientHandleService.execute', {
         "method": "rewardPayment",
         "data": {
             "channel": "1",
             "clientTime": int(time.time() * 1000),
             "uuid": uuid,
             "videoTimeLength": video_time_length,
             "messageType": "2",
             "activeType": active_type,
             "activeId": active_id
         }
     }, cookie)
    resp = requests.get(url=url_str, headers=headers)
    print("resp = ", resp.content.decode("utf-8"))
    try:
        if safe_get(resp.content):
            data = json.loads(resp.content)
            if data.code == 0 & data.isSuccess:
                user_info.score += data.data.reward
                print(f'{user_info.taskName}任务完成，获得${data.data.reward}金币')
            else:
                print(f'{user_info.taskName}任务失败，{data.message}')
    except Exception as e:
        logging.exception(e)


def cash():
    url_str, headers = task_url('MyAssetsService.execute', {
        "method": "userCashRecord",
        "data": {
            "channel": 1,
            "pageNum": 1,
            "pageSize": 20
        }
    }, cookie)
    resp = requests.get(url=url_str, headers=headers)
    print("resp = ", resp.content.decode("utf-8"))
    try:
        if safe_get(resp.content):
            data = json.loads(resp.content)
            user_info.total = data.data.goldBalance
    except Exception as e:
        logging.exception(e)


# 大转盘
def wheels_home():
    usl_str, headers = task_get_url('wheelsHome', {"linkId": "toxw9c5sy9xllGBr3QFdYg"}, cookie)
    resp = requests.get(url=usl_str, headers=headers)
    print("resp = ", resp.content.decode("utf-8"))
    try:
        if safe_get(resp.content):
            data = json.loads(resp.content);
            if data.code == 0:
                print(f'【幸运大转盘】剩余抽奖机会：{data.data.lotteryChances}')
                chances = data.data.lotteryChances
                while chances > 0:
                    wheels_lottery()
                    user_info.wait(500)
                    chances = chances - 1
    except Exception as e:
        logging.exception(e)


# 大转盘
def wheels_lottery():
    usl_str, headers = task_get_url('wheelsLottery', {"linkId": "toxw9c5sy9xllGBr3QFdYg"}, cookie)
    resp = requests.get(url=usl_str, headers=headers)
    print("resp = ", resp.content.decode("utf-8"))
    try:
        if safe_get(resp.content):
            data = json.loads(resp.content)
            if data.data & data.data.rewardType:
                print(
                    f'幸运大转盘抽奖获得：【{data.data.couponUsedValue}-{data.data.rewardValue}{data.data.couponDesc}】\n')
                global message, jd_global
                message += f'幸运大转盘抽奖获得：【{data.data.couponUsedValue}-{data.data.rewardValue}{data.data.couponDesc}】\n'
            else:
                print(f'幸运大转盘抽奖获得：空气')
    except Exception as e:
        logging.exception(e)


# 大转盘任务
def ap_task_ist():
    usl_str, headers = task_get_url('apTaskList', {"linkId": "toxw9c5sy9xllGBr3QFdYg"}, cookie)
    resp = requests.get(url=usl_str, headers=headers)
    print("resp = ", resp.content.decode("utf-8"))
    try:
        if safe_get(resp.content):
            data = json.loads(resp.content)
            if data.code == 0:
                for TASK in data.data:
                    # {"linkId":"toxw9c5sy9xllGBr3QFdYg","taskType":"SIGN","taskId":67,"channel":4}
                    if not TASK.taskFinished & TASK.taskType in ['SIGN', 'BROWSE_CHANNEL']:
                        print(f'去做任务{TASK.taskTitle}')
                        ap_do_task(TASK.taskType, TASK.id, 4, TASK.taskSourceUrl)
    except Exception as ex:
        logging.exception(ex)


# 大转盘做任务
def ap_do_task(taskType, taskId, channel, itemId):
    # print({"linkId":"toxw9c5sy9xllGBr3QFdYg","taskType":taskType,"taskId":taskId,"channel":channel,"itemId":itemId})
    usl_str, headers = task_get_url('apDoTask', {
        "linkId": "toxw9c5sy9xllGBr3QFdYg",
        "taskType": taskType,
        "taskId": taskId,
        "channel": channel,
        "itemId": itemId
    }, cookie)
    resp = requests.get(url=usl_str, headers=headers)
    print("resp = ", resp.content.decode("utf-8"))
    try:
        if safe_get(resp.content):
            data = json.loads(resp.content)
            if data.code == 0 & data.data & data.data.finished:
                print(f'任务完成成功')
            else:
                print(json.dumps(data))
    except Exception as e:
        logging.exception(e)


# 红包大富翁
def rich_man_index():
    usl_str, headers = task_url('richManIndex', {"actId": "hbdfw", "needGoldToast": "True"}, cookie)
    resp = requests.get(url=usl_str, headers=headers)
    print("resp = ", resp.content.decode("utf-8"))
    try:
        if safe_get(resp.content):
            data = json.loads(resp.content)
            if data.code == 0 and data['data'] and data['data']['userInfo']:
                userInfo = data['data']['userInfo']
                print(f'用户当前位置：{userInfo.position}，剩余机会：{userInfo.randomTimes}')
                times = userInfo.randomTimes
                while times >= 0:
                    shoot_rich_man_dice()
                    times -= 1
    except Exception as e:
        logging.exception(e)


# 红包大富翁
def shoot_rich_man_dice():
    usl_str, headers = task_url('shootRichManDice', {"actId": "hbdfw"}, cookie)
    resp = requests.get(url=usl_str, headers=headers)
    print("result", resp.content.decode("utf-8"))
    try:
        if safe_get(resp.content):
            data = json.loads(resp.content)
            if data.code == 0 and data['data'] and data['data']['rewardType'] and data['data']['couponDesc']:
                data_info = data['data']
                global message
                message += f'红包大富翁抽奖获得：【{data_info.couponUsedValue}-{data_info.rewardValue} {data_info.poolName}】\n'
                print(f'红包大富翁抽奖获得：【{data_info.couponUsedValue}-{data_info.rewardValue} {data_info.poolName}】')
            else:
                print(f'红包大富翁抽奖：获得空气')
    except Exception as ex:
        logging.exception(ex)


def order_reward(item_type=0):

    timestamp = int(time.time() * 1000)
    headers = {
        'Host': 'api.m.jd.com',
        'accept': 'application/json, text/plain, */*',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://palace.m.jd.com',
        'accept-language': 'zh-cn',
        'user-agent': "'jdltapp;iPad;3.1.0;14.4;network/wifi;Mozilla/5.0 (iPad; CPU OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/1",
        'referer': 'https://palace.m.jd.com/?lng=110.917107&lat=22.2706&sid=abefac3cfbcb550b542e4c064dbcabfw&un_area=19_1684_1687_6233',
        'Cookie': cookie
    }
    if item_type > 0:
        data_string = 'functionId=OrderRewardService&body={"method":"receiveReward","data":{"orderQty":' + item_type.__str__() + '}}&_t=' + timestamp.__str__() + '&appid=market-task-h5&eid='
    else:
        data_string = 'functionId=OrderRewardService&body={"method":"queryRewards","data":{}}&_t={t}&appid=market-task-h5&eid='
    url_str = 'https://api.m.jd.com/' + data_string

    resp = requests.post(url=url_str, headers=headers)
    print("res=" + resp.content.decode(encoding="utf-8"))
    try:
        if safe_get(resp.content):
            data = json.loads(resp.content)
            print(data)
            if data.code == 0 & data.isSuccess:
                if data.data.details:
                    user_info.details = data.data.details
                    for item in user_info.details:
                        if item.status == 2:
                            print(f'\n检测到【下单领红包】有奖励可领取，开始领取奖励')
                            order_reward(item.orderQty);
                            user_info.wait(2000)
                        elif item.status == 1:
                            print(
                                f'\n【下单领红包】暂无奖励可领取，再下${data.data.needOrderQty}单可领取${data.data.rewardAmount}元')
                            break
                else:
                    if data.code == 0:
                        print(f'奖励领取结果，获得${data.data.rewardAmount}元')
                    else:
                        print(f'奖励领取结果：获得${json.dumps(data)}')
            else:
                print(f'\n其他情况：{json.dumps(data)}')
    except Exception as ex:
        logging.exception(ex)


def invite2():
    inviter_id_arr = [
        "o63wN5qAZ/k8MYBfzVVkzJpwsM5V0a5t21tduAM0Ybc=",
        "tfk6jlhVkWW4BQenfFQ4tMV1r3jAgvODvT0E65oefUA="
    ]
    inviter_id = inviter_id_arr[random.randint(0, len(inviter_id_arr) - 1)]
    url_str = "https://api.m.jd.com/"
    body = {
        "method": "participateInviteTask",
        "data": {
            "channel": "1",
            "encryptionInviterPin": inviter_id,
            "type": 1
        }
    }
    body_str = f'functionId=TaskInviteService&body={json.dumps(body)}&appid=market-task-h5&uuid=' + f'&_t={int(time.time() * 1000)}'
    headers = {
        "Host": "api.m.jd.com",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://assignment.jd.com",
        "Accept-Language": "zh-CN,zh-Hans;q=0.9",
        "User-Agent": "'jdltapp;iPad;3.1.0;14.4;network/wifi;Mozilla/5.0 (iPad; CPU OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/1",
        "Referer": "https://assignment.jd.com/",
        "Accept-Encoding": "gzip, deflate, br",
        "Cookie": cookie
    }
    resp = requests.post(url_str, headers=headers, data=body_str)
    print("result=", resp.content.decode("utf-8"))


def invite():
    t = int(time.time() * 1000)
    inviter_id_arr = [
        "o63wN5qAZ/k8MYBfzVVkzJpwsM5V0a5t21tduAM0Ybc=",
        "tfk6jlhVkWW4BQenfFQ4tMV1r3jAgvODvT0E65oefUA="
    ]
    inviter_id = inviter_id_arr[(random.randint(0, len(inviter_id_arr) - 1))]
    url_str = f'https://api.m.jd.com/?t={t}'
    body = {
        "method": "attendInviteActivity",
        "data": {
            "inviterPin": inviter_id,
            "channel": 1,
            "token": "",
            "frontendInitStatus": ""
        }
    }
    body_str = f'functionId=InviteFriendChangeAssertsService&body={json.dumps(body)}&referer=-1&eid=eidI9b2981202fsec83iRW1nTsOVzCocWda3YHPN471AY78%2FQBhYbXeWtdg%2F3TCtVTMrE1JjM8Sqt8f2TqF1Z5P%2FRPGlzA1dERP0Z5bLWdq5N5B2VbBO&aid=&client=ios&clientVersion=14.4.2&networkType=wifi&fp=-1&uuid=ab048084b47df24880613326feffdf7eee471488&osVersion=14.4.2&d_brand=iPhone&d_model=iPhone10,2&agent=-1&pageClickKey=-1&platform=3&lang=zh_CN&appid=market-task-h5&_t={t}'
    headers = {
        "Host": "api.m.jd.com",
        "Accept": "application/json, text/plain, */*",
        "Content-type": "application/x-www-form-urlencoded",
        "Origin": "https://invite-reward.jd.com",
        "Accept-Language": "zh-CN,zh-Hans;q=0.9",
        "User-Agent": "'jdltapp;iPad;3.1.0;14.4;network/wifi;Mozilla/5.0 (iPad; CPU OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/1",
        "Referer": 'https://invite-reward.jd.com/',
        "Accept-Encoding": "gzip, deflate, br",
        "Cookie": cookie
    }
    resp = requests.post(url_str, headers=headers, data=body_str)
    print("res = " + resp.content.decode("utf-8"))


def total_bean():
    url_str = 'https://wq.jd.com/user/info/QueryJDUserInfo?sceneval=2'
    headers = {
        "Accept": "application/json,text/plain, */*",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-cn",
        "Connection": "keep-alive",
        "Cookie": cookie,
        "Referer": "https://wqs.jd.com/my/jingdou/my.shtml?sceneval=2",
        "User-Agent": "jdapp;iPhone;9.4.4;14.3;network/4g;Mozilla/5.0 (iPhone; CPU iPhone OS 14_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/1"
    }
    resp = requests.post(url_str, headers=headers)
    print("result=", resp.content.decode("utf-8"))
    try:
        content = resp.content
        if content:
            data = json.loads(content)
            print(data)
            if data['retcode'] == 13:
                user_info.isLogin = False  # cookie过期
                return

            if data['retcode'] == 0:
                base_ = data['base']
                user_info.nickName = base_['nickname'] if len(base_) & len(base_['nickname']) > 0 else user_info.UserName
            else:
                user_info.nickName = user_info.UserName
        else:
            print('京东服务器返回空数据')
    except Exception as ex:
        logging.exception(ex)


def enter():
    global user_info
    if len(cookiesArr[0]):
        user_info.msg(user_info.name, '【提示】请先获取京东账号一cookie\n直接使用NobyDa的京东签到获取',
                      'https://bean.m.jd.com/bean/signIndex.action',
                      {"open-url": "https://bean.m.jd.com/bean/signIndex.action"})
        return
    for i in range(0, len(cookiesArr)):
        try:
            if cookiesArr[i]:
                global cookie
                cookie = cookiesArr[i]
                p = re.compile(r'pt_pin=([^;]+)(?=;?)')
                res = p.findall(cookie)
                user_info.UserName = res[0]
                user_info.index = i + 1
                user_info.isLogin = True
                user_info.nickName = ''
                total_bean()
                print_name = user_info.nickName if len(user_info.nickName) > 0 else user_info.UserName
                print(f'\n******开始【京东账号${user_info.index}】{print_name}*********\n')
                if not user_info.isLogin:
                    user_info.msg(user_info.name, '【提示】cookie已失效',
                                  f'京东账号${user_info.index} {print_name}\n请重新登录获取\nhttps://bean.m.jd.com/bean/signIndex.action',
                                  {"open-url": "https://bean.m.jd.com/bean/signIndex.action"})
                    continue

                jd_global()
                user_info.wait(2 * 1000)
                if IPError:
                    print(f'403 黑IP了，换IP或等一段时间')
                    break
        except Exception as e:
            user_info.log('', f'❌ {user_info.name}, 失败! 原因: {e}!', '')
        finally:
            user_info.done()



if __name__ == '__main__':
    # total_bean()
    # rich_man_index()
    # shoot_rich_man_dice()
    # invite2()
    # wheels_home()
    # sign()
    # sign_init()
    # task_list()
    query_joy()

