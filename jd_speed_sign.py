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
import datetime
import json
import logging
import time

import requests

import sendNotify

notify = sendNotify
# Node.js用户请在jdCookie.js处填写京东ck;
# jdCookieNode = require('./jdCookie.js') : ''
jdCookieNode = ''
cookiesArr = []
cookie = ''
message = ''
IPError = False #403 ip黑
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
# !(() => {
#   if (!cookiesArr[0]) {
#     user_info.msg(user_info.name, '【提示】请先获取京东账号一cookie\n直接使用NobyDa的京东签到获取', 'https://bean.m.jd.com/bean/signIndex.action', {"open-url": "https://bean.m.jd.com/bean/signIndex.action"});
#     return;
#   }
#    date = datetime.datetime.now()
  user_info.last_day = new Date(date.getFullYear(), date.getMonth()+1, 0).getDate() == date.getDate()
#   for (i = 0; i < cookiesArr.length; i++) {
#     if (cookiesArr[i]) {
#       cookie = cookiesArr[i];
#       user_info.UserName = decodeURIComponent(cookie.match(/pt_pin=([^; ]+)(?=;?)/) & cookie.match(/pt_pin=([^; ]+)(?=;?)/)[1])
#       user_info.index = i + 1;
#       user_info.isLogin = True;
#       user_info.nickName = '';
#       message = '';
#       TotalBean();
#       print(f'\n******开始【京东账号${user_info.index}】{user_info.nickName || user_info.UserName}*********\n');
#       if (!user_info.isLogin) {
#         user_info.msg(user_info.name, `【提示】cookie已失效`, `京东账号${user_info.index} {user_info.nickName || user_info.UserName}\n请重新登录获取\nhttps://bean.m.jd.com/bean/signIndex.action`, { "open-url": "https://bean.m.jd.com/bean/signIndex.action" });
# 
#         if (user_info.isNode()) {
#           notify.sendNotifyf'{user_info.name}cookie已失效 - {user_info.UserName}`, `京东账号${user_info.index} {user_info.UserName}\n请重新登录获取cookie');
#         }
#         continue
#       }
#       jdGlobal()
#       user_info.wait(2*1000)
#       if (IPError){
#         print(f'403 黑IP了，换IP或等一段时间');
#         break;
#       }
#     }
#   }
# })()
#   .catch((e) => {
#     user_info.log('', `❌ {user_info.name}, 失败! 原因: {e}!`, '')
#   })
#   .finally(() => {
#     user_info.done();
#   })


class UserInfo(object):

  def __init__(self):
    self.score = 0
    self.name = ''
    self.total = 0
    self.index = 0
    self.nickName = 0
    self.isLogin = False

  def wait(self, param):
    time.sleep(1)


user_info = UserInfo()


def safe_get(content):
  try:
    if isinstance(content, dict):
      return True
  except Exception as e:
    logging.exception(e)
    print('京东服务器访问数据为空，请检查自身设备网络情况')
    return False


def jd_global():
  try:
    richManIndex()

    wheels_home()
    ap_task_ist()
    wheels_home()

    #await signInit()
    #await sign()
    invite()
    invite2()
    score = 0
    total = 0
    task_list()
    query_joy()
    #await signInit()
    cash()
    if last_day:
      print('月底了,自动领下单红包奖励')
      orderReward()
    show_msg()
  except Exception as e:
    logging.exception(e)


def show_msg():
    message += f'本次运行获得{user_info.score}金币，共计{user_info.total}金币\n可兑换 {(user_info.total/10000).toFixed(2)} 元京东红包\n兑换入口：京东极速版->我的->金币'
    print(user_info.name, '', f'京东账号{user_info.index}{user_info.nickName}\n{message}')


def assemble_request(function_id, req_body):
  return f"functionId={function_id}&body{json.dumps(req_body)}"


def sign_init():
  resp = requests.get(assemble_request('speedSignInit', {
    "activityId": "8a8fabf3cccb417f8e691b6774938bc2",
    "kernelPlatform": "RN",
    "inviterId": "U44jAghdpW58FKgfqPdotA=="
  }))
  print(resp.content)
  try:
    # if err:
    # print(f'{json.dumps(err)}')
    # print(f'{user_info.name} API请求失败，请检查网路重试')
    # else:
    if safe_get(resp.content):
      data = json.loads(resp.content)
      print(data)
  except Exception as e:
    logging.exception(e)


def sign():
  resp = requests.get(assemble_request('speedSign', {
    "kernelPlatform": "RN",
    "activityId": "8a8fabf3cccb417f8e691b6774938bc2",
    "noWaitPrize": "False"
  }))
  print(resp.content)
  try:
    if safe_get(resp.content):
      data = json.loads(resp.content)
      if data['subCode'] == 0:
        print(f'签到获得{data.data.signAmount}现金，共计获得{data.data.cashDrawAmount}')
      else:
        print(f'签到失败，{data.msg}')
  except Exception as e:
    logging.exception(e)


def task_list():
  resp = requests.get(assemble_request('ClientHandleService.execute', {
    "version": "3.1.0",
    "method": "newTaskCenterPage",
    "data": {"channel": 1}
  }))
  print(resp.content)
  try:
    if safe_get(resp.content):
      data = json.loads(resp.content);
      for task in data.data:
        user_info['taskName'] = task.taskInfo.mainTitle
        if task.taskInfo.status == 0:
          if task.taskType >= 1000:
            do_task(task.taskType)
            time.sleep(1)
          else:
            user_info['canStartNewItem '] = True
            while user_info['canStartNewItem']:
              if task.taskType != 3:
                query_item(task.taskType)
              else:
                start_item("", task.taskType)
        else:
          print(f'{task.taskInfo.mainTitle}已完成')
        if IPError:
          logging.error('API请求失败，停止执行')
          break
  except Exception as e:
    logging.exception(e)


def do_task(taskId):
  resp = requests.get(assemble_request('ClientHandleService.execute', {
      "method": "marketTaskRewardPayment",
      "data": {"channel": 1, "clientTime": + datetime.datetime.now() + 0.588, "activeType": taskId}
    }))
  print(resp.content)
  try:
      if safe_get(resp.content):
        data = json.loads(resp.content);
        if data.code == 0:
          print(f'{data.data.taskInfo.mainTitle}任务完成成功，预计获得${data.data.reward}金币')
        else:
          print(f'任务完成失败，{data.message}')
  except Exception as e:
    logging.exception(e)


def query_joy():
    resp = requests.get(assemble_request('ClientHandleService.execute', {"method": "queryJoyPage", "data": {"channel": 1}}))
    print("resp = ", resp.content)
    try:
        if safe_get(resp.content):
          data = json.loads(resp.content)
          if data.data.taskBubbles:
            for task in data.data.taskBubbles:
              reward_task(task.id, task.activeType)
              user_info.wait(500)
    except Exception as e:
      logging.exception(e)


def reward_task(task_id, active_type):
  resp = requests.get(assemble_request('ClientHandleService.execute', {
    "method": "joyTaskReward",
    "data": {"id": task_id, "channel": 1, "clientTime": + datetime.datetime.now() + 0.588, "activeType": active_type}
  }))
  print("resp = ", resp.content)
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
  resp = requests.get(assemble_request('ClientHandleService.execute', {
    "method": "queryNextTask",
    "data": {"channel": 1, "activeType": active_type}
  }))
  print("resp = ", resp.content)
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
  resp = requests.get(assemble_request('ClientHandleService.execute', {
    "method": "enterAndLeave",
    "data": {
      "activeId": active_id,
      "clientTime": + datetime.datetime.now(),
      "channel": "1",
      "messageType": "1",
      "activeType": active_type,
    }
  }))
  print("resp = ", resp.content)
  try:
    if safe_get(resp.content):
      data = json.loads(resp.content);
      if data.code == 0 & data.data:
        if data.data.taskInfo.isTaskLimit == 0:
          param = data.data.taskInfo
          if active_type != 3:
            param["videoBrowsing"] = 5 if active_type == 1 else 10
          print(f'【{param["taskCompletionProgress"] + 1}/{param["taskCompletionLimit"]}】浏览商品任务记录成功，等待{param["videoBrowsing"]}秒')
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
      

def end_item(uuid, active_type, active_id ="", video_time_length =""):
    resp = requests.get(assemble_request('ClientHandleService.execute',
      {
        "method": "enterAndLeave",
        "data": {
          "channel": "1",
          "clientTime": +datetime.datetime.now(),
          "uuid": uuid,
          "videoTimeLength": video_time_length,
          "messageType": "2",
          "activeType": active_type,
          "activeId": active_id
        }
      }))
    print("resp = ", resp.content)
    try:
        if safe_get(resp.content):
          data = json.loads(resp.content);
          if data.code == 0 & data.isSuccess:
            reward_item(uuid, active_type, active_id, video_time_length)
          else:
            print(f'{user_info.taskName}任务结束失败，{data.message}')
    except Exception as e:
      logging.exception(e)


def reward_item(uuid, active_type, active_id="", video_time_length=""):
  resp = requests.get(assemble_request('ClientHandleService.execute',
                                       {
                                         "method": "rewardPayment",
                                         "data": {
                                           "channel": "1",
                                           "clientTime": +datetime.datetime.now(),
                                           "uuid": uuid,
                                           "videoTimeLength": video_time_length,
                                           "messageType": "2",
                                           "activeType": active_type,
                                           "activeId": active_id
                                         }
                                       }))
  print("resp = ", resp.content)
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
  resp = requests.get(assemble_request('MyAssetsService.execute',
                                       {"method": "userCashRecord",
                                        "data": {"channel": 1, "pageNum": 1, "pageSize": 20}
                                        }))
  print("resp = ", resp.content)
  try:
    if safe_get(resp.content):
      data = json.loads(resp.content);
      user_info.total = data.data.goldBalance
  except Exception as e:
    logging.exception(e)
       

#大转盘
def wheels_home():
    resp = requests.get(assemble_request('wheelsHome',
      {"linkId":"toxw9c5sy9xllGBr3QFdYg"}))
    print("resp = ", resp.content)
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


#大转盘
def wheels_lottery():
  resp = requests.get(assemble_request('wheelsLottery',
                                       {"linkId": "toxw9c5sy9xllGBr3QFdYg"}))
  print("resp = ", resp.content)
  try:
    if safe_get(resp.content):
      data = json.loads(resp.content)
      if data.data & data.data.rewardType:
        print(f'幸运大转盘抽奖获得：【{data.data.couponUsedValue}-{data.data.rewardValue}{data.data.couponDesc}】\n')
        message += f'幸运大转盘抽奖获得：【{data.data.couponUsedValue}-{data.data.rewardValue}{data.data.couponDesc}】\n'
      else:
        print(f'幸运大转盘抽奖获得：空气')
  except Exception as e:
    logging.exception(e)
        
        
#大转盘任务
def ap_task_ist():
  resp = requests.get(assemble_request('apTaskList',
                                       {"linkId": "toxw9c5sy9xllGBr3QFdYg"}))
  print("resp = ", resp.content)
  try:
    if safe_get(resp.content):
      data = json.loads(resp.content)
      if data.code == 0:
        for task in data.data:
          # {"linkId":"toxw9c5sy9xllGBr3QFdYg","taskType":"SIGN","taskId":67,"channel":4}
          if !task.taskFinished & task.taskType in['SIGN', 'BROWSE_CHANNEL']:
            print(f'去做任务{task.taskTitle}')
            apdo_task(task.taskType, task.id, 4, task.taskSourceUrl)
  except Exception as e:
    logging.exception(e)


#大转盘做任务
def apdo_task(taskType,taskId,channel,itemId) {
  #print({"linkId":"toxw9c5sy9xllGBr3QFdYg","taskType":taskType,"taskId":taskId,"channel":channel,"itemId":itemId})
  
    requests.get(assemble_request('apdo_task',
      {"linkId":"toxw9c5sy9xllGBr3QFdYg","taskType":taskType,"taskId":taskId,"channel":channel,"itemId":itemId}),
      
        try:
          if err:
            print(f'{json.dumps(err)}')
            print(f'{user_info.name} API请求失败，请检查网路重试')
          else:
            if safe_get(resp.content):
              data = json.loads(resp.content)
              if(data.code ==0 & data.data & data.data.finished){
                print(f'任务完成成功')
              else:
                print(json.dumps(data))
              }
            }
          }
        except Exception as e:
          logging.exception(e)
        } finally {
          resolve(data);
        }
      })
  })
}
#红包大富翁
def richManIndex() {
  
    requests.get(assemble_request('richManIndex', {"actId":"hbdfw","needGoldToast":"True"})
      try:
        if err:
          print(f'{json.dumps(err)}')
          print(f'{user_info.name} API请求失败，请检查网路重试')
        else:
          if safe_get(resp.content):
            data = json.loads(resp.content)
            if(data.code ==0 & data.data & data.data.userInfo){
              print(f'用户当前位置：{data.data.userInfo.position}，剩余机会：{data.data.userInfo.randomTimes}')
              while(data.data.userInfo.randomTimes--){
                shootRichManDice()
              }
            }
          }
        }
      except Exception as e:
        logging.exception(e)
      } finally {
        resolve(data);
      }
    })
  })
}
#红包大富翁
def shootRichManDice() {
  
    requests.get(assemble_request('shootRichManDice', {"actId":"hbdfw"})
      try:
        if err:
          print(f'{json.dumps(err)}')
          print(f'{user_info.name} API请求失败，请检查网路重试')
        else:
          if safe_get(resp.content):
            data = json.loads(resp.content)
            if(data.code ==0 & data.data & data.data.rewardType & data.data.couponDesc){
              message += `红包大富翁抽奖获得：【{data.data.couponUsedValue}-{data.data.rewardValue} {data.data.poolName}】\n`
              print(f'红包大富翁抽奖获得：【{data.data.couponUsedValue}-{data.data.rewardValue} {data.data.poolName}】')
            else:
              print(f'红包大富翁抽奖：获得空气')
            }
          }
        }
      except Exception as e:
        logging.exception(e)
      } finally {
        resolve(data);
      }
    })
  })
}
def orderReward(type) {
  t = +datetime.datetime.now()
  var headers = {
    'Host': 'api.m.jd.com',
    'accept': 'application/json, text/plain, */*',
    'content-type': 'application/x-www-form-urlencoded',
    'origin': 'https://palace.m.jd.com',
    'accept-language': 'zh-cn',
    'user-agent': user_info.isNode() ? (process.env.JS_USER_AGENT ? process.env.JS_USER_AGENT : (require('./JS_USER_AGENTS').USER_AGENT)) : (user_info.getdata('JSUA') ? user_info.getdata('JSUA') : "'jdltapp;iPad;3.1.0;14.4;network/wifi;Mozilla/5.0 (iPad; CPU OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/1"),
    'referer': 'https://palace.m.jd.com/?lng=110.917107&lat=22.2706&sid=abefac3cfbcb550b542e4c064dbcabfw&un_area=19_1684_1687_6233',
    'Cookie': cookie
  };
  if (type) {
    var dataString = `functionId=OrderRewardService&body={"method":"receiveReward","data":{"orderQty":{type}}}&_t={t}&appid=market-task-h5&eid=`;
  else:
    var dataString = `functionId=OrderRewardService&body={"method":"queryRewards","data":{}}&_t={t}&appid=market-task-h5&eid=`;
  }
  var options = {
    url: `https://api.m.jd.com/`,
    headers: headers,
    body: dataString
  };
  user_info.post(options
    try:
      if err:
        print(f'{json.dumps(err)}')
        print(f'orderReward API请求失败，请检查网路重试')
      else:
        if safe_get(resp.content):
          data = json.loads(resp.content)
          if (data.code == 0 & data.isSuccess) {
            if (data.data.details) {
              user_info.details = data.data.details
              for (item of user_info.details) {
                if (item.status == 2) {
                  print(f'\n检测到【下单领红包】有奖励可领取，开始领取奖励')
                  orderReward(item.orderQty);
                  user_info.wait(2000)
                } else if (item.status == 1) {
                  print(f'\n【下单领红包】暂无奖励可领取，再下${data.data.needOrderQty}单可领取${data.data.rewardAmount}元')
                  break
                }
              }
            else:
              if (data.code == 0) {
                print(f'奖励领取结果，获得${data.data.rewardAmount}元')
              else:
                print(f'奖励领取结果：获得${json.dumps(data)}')
              }
            }
          else:
            print(f'\n其他情况：{json.dumps(data)}')
          }
        }
      }
    except Exception as e:
      logging.exception(e)
    }
  })
}


var __encode = 'jsjiami.com', _a = {}, _0xb483 = ["\x5F\x64\x65\x63\x6F\x64\x65", "\x68\x74\x74\x70\x3A\x2F\x2F\x77\x77\x77\x2E\x73\x6F\x6A\x73\x6F\x6E\x2E\x63\x6F\x6D\x2F\x6A\x61\x76\x61\x73\x63\x72\x69\x70\x74\x6F\x62\x66\x75\x73\x63\x61\x74\x6F\x72\x2E\x68\x74\x6D\x6C"]; (def (_0xd642x1) { _0xd642x1[_0xb483[0]] = _0xb483[1] })(_a); var __Oxb24bc = ["\x6C\x69\x74\x65\x2D\x61\x6E\x64\x72\x6F\x69\x64\x26", "\x73\x74\x72\x69\x6E\x67\x69\x66\x79", "\x26\x61\x6E\x64\x72\x6F\x69\x64\x26\x33\x2E\x31\x2E\x30\x26", "\x26", "\x26\x38\x34\x36\x63\x34\x63\x33\x32\x64\x61\x65\x39\x31\x30\x65\x66", "\x31\x32\x61\x65\x61\x36\x35\x38\x66\x37\x36\x65\x34\x35\x33\x66\x61\x66\x38\x30\x33\x64\x31\x35\x63\x34\x30\x61\x37\x32\x65\x30", "\x69\x73\x4E\x6F\x64\x65", "\x63\x72\x79\x70\x74\x6F\x2D\x6A\x73", "", "\x61\x70\x69\x3F\x66\x75\x6E\x63\x74\x69\x6F\x6E\x49\x64\x3D", "\x26\x62\x6F\x64\x79\x3D", "\x26\x61\x70\x70\x69\x64\x3D\x6C\x69\x74\x65\x2D\x61\x6E\x64\x72\x6F\x69\x64\x26\x63\x6C\x69\x65\x6E\x74\x3D\x61\x6E\x64\x72\x6F\x69\x64\x26\x75\x75\x69\x64\x3D\x38\x34\x36\x63\x34\x63\x33\x32\x64\x61\x65\x39\x31\x30\x65\x66\x26\x63\x6C\x69\x65\x6E\x74\x56\x65\x72\x73\x69\x6F\x6E\x3D\x33\x2E\x31\x2E\x30\x26\x74\x3D", "\x26\x73\x69\x67\x6E\x3D", "\x61\x70\x69\x2E\x6D\x2E\x6A\x64\x2E\x63\x6F\x6D", "\x2A\x2F\x2A", "\x52\x4E", "\x4A\x44\x4D\x6F\x62\x69\x6C\x65\x4C\x69\x74\x65\x2F\x33\x2E\x31\x2E\x30\x20\x28\x69\x50\x61\x64\x3B\x20\x69\x4F\x53\x20\x31\x34\x2E\x34\x3B\x20\x53\x63\x61\x6C\x65\x2F\x32\x2E\x30\x30\x29", "\x7A\x68\x2D\x48\x61\x6E\x73\x2D\x43\x4E\x3B\x71\x3D\x31\x2C\x20\x6A\x61\x2D\x43\x4E\x3B\x71\x3D\x30\x2E\x39", "\x75\x6E\x64\x65\x66\x69\x6E\x65\x64", "\x6C\x6F\x67", "\u5220\u9664", "\u7248\u672C\u53F7\uFF0C\x6A\x73\u4F1A\u5B9A", "\u671F\u5F39\u7A97\uFF0C", "\u8FD8\u8BF7\u652F\u6301\u6211\u4EEC\u7684\u5DE5\u4F5C", "\x6A\x73\x6A\x69\x61", "\x6D\x69\x2E\x63\x6F\x6D"]; def assemble_request(_0x7683x2, _0x7683x3 = {}) { _0x7683x4 = + datetime.datetime.now(); _0x7683x5 = `{__Oxb24bc[0x0]}{JSON[__Oxb24bc[0x1]](_0x7683x3)}{__Oxb24bc[0x2]}{_0x7683x2}{__Oxb24bc[0x3]}{_0x7683x4}{__Oxb24bc[0x4]}`; _0x7683x6 = __Oxb24bc[0x5];  _0x7683x7 = user_info[__Oxb24bc[0x6]]() ? require(__Oxb24bc[0x7]) : CryptoJS; _0x7683x8 = _0x7683x7.HmacSHA256(_0x7683x5, _0x7683x6).toString(); return { url: `{__Oxb24bc[0x8]}{JD_API_HOST}{__Oxb24bc[0x9]}{_0x7683x2}{__Oxb24bc[0xa]}{escape(JSON[__Oxb24bc[0x1]](_0x7683x3))}{__Oxb24bc[0xb]}{_0x7683x4}{__Oxb24bc[0xc]}{_0x7683x8}{__Oxb24bc[0x8]}`, headers: { '\x48\x6F\x73\x74': __Oxb24bc[0xd], '\x61\x63\x63\x65\x70\x74': __Oxb24bc[0xe], '\x6B\x65\x72\x6E\x65\x6C\x70\x6C\x61\x74\x66\x6F\x72\x6D': __Oxb24bc[0xf], '\x75\x73\x65\x72\x2D\x61\x67\x65\x6E\x74': __Oxb24bc[0x10], '\x61\x63\x63\x65\x70\x74\x2D\x6C\x61\x6E\x67\x75\x61\x67\x65': __Oxb24bc[0x11], '\x43\x6F\x6F\x6B\x69\x65': cookie } } } (def (_0x7683x9, _0x7683xa, _0x7683xb, _0x7683xc, _0x7683xd, _0x7683xe) { _0x7683xe = __Oxb24bc[0x12]; _0x7683xc = def (_0x7683xf) { if (typeof alert !== _0x7683xe) { alert(_0x7683xf) }; if (typeof console !== _0x7683xe) { console[__Oxb24bc[0x13]](_0x7683xf) } }; _0x7683xb = def (_0x7683x7, _0x7683x9) { return _0x7683x7 + _0x7683x9 }; _0x7683xd = _0x7683xb(__Oxb24bc[0x14], _0x7683xb(_0x7683xb(__Oxb24bc[0x15], __Oxb24bc[0x16]), __Oxb24bc[0x17])); try: _0x7683x9 = __encode; if (!(typeof _0x7683x9 !== _0x7683xe & _0x7683x9 == _0x7683xb(__Oxb24bc[0x18], __Oxb24bc[0x19]))) { _0x7683xc(_0x7683xd) } except Exception as e: _0x7683xc(_0x7683xd) } })({})

def assemble_request(function_id, body) {
  return {
    url: `https://api.m.jd.com/?appid=activities_platform&functionId={function_id}&body={escape(json.dumps(body))}&t={+datetime.datetime.now()}`,
    headers: {
      'Cookie': cookie,
      'Host': 'api.m.jd.com',
      'Accept': '*/*',
      'Connection': 'keep-alive',
      'user-agent': user_info.isNode() ? (process.env.JS_USER_AGENT ? process.env.JS_USER_AGENT : (require('./JS_USER_AGENTS').USER_AGENT)) : (user_info.getdata('JSUA') ? user_info.getdata('JSUA') : "'jdltapp;iPad;3.1.0;14.4;network/wifi;Mozilla/5.0 (iPad; CPU OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/1"),
      'Accept-Language': 'zh-Hans-CN;q=1,en-CN;q=0.9',
      'Accept-Encoding': 'gzip, deflate, br',
      'Content-Type': "application/x-www-form-urlencoded",
      "referer": "https://an.jd.com/babelDiy/Zeus/q1eB6WUB8oC4eH1BsCLWvQakVsX/index.html"
    }
  }
}

def invite2() {
  inviterIdArr = [
    "pVbNk9xIuI02DeRtwUiztA==",
    "s4UuZYFN6GW3jbg4x9Z8LA==",
    "Vf+kZwVHm4/P5/ZkyCY+DA==",
    "4y1yGPA4HCaFNCw8BZ6gsw=="
  ]
  inviterId = inviterIdArr[Math.floor((Math.random() * inviterIdArr.length))]
  options = {
    url: "https://api.m.jd.com/",
    body: `functionId=TaskInviteService&body={json.dumps({"method":"participateInviteTask","data":{"channel":"1","encryptionInviterPin":encodeURIComponent(inviterId),"type":1}})}&appid=market-task-h5&uuid=&_t={Date.now()}`,
    headers: {
      "Host": "api.m.jd.com",
      "Accept": "application/json, text/plain, */*",
      "Content-Type": "application/x-www-form-urlencoded",
      "Origin": "https://assignment.jd.com",
      "Accept-Language": "zh-CN,zh-Hans;q=0.9",
      "User-Agent": user_info.isNode() ? (process.env.JS_USER_AGENT ? process.env.JS_USER_AGENT : (require('./JS_USER_AGENTS').USER_AGENT)) : (user_info.getdata('JSUA') ? user_info.getdata('JSUA') : "'jdltapp;iPad;3.1.0;14.4;network/wifi;Mozilla/5.0 (iPad; CPU OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/1"),
      "Referer": "https://assignment.jd.com/",
      "Accept-Encoding": "gzip, deflate, br",
      "Cookie": cookie
    }
  }
  user_info.post(options, 
    #print(data)
  })
}

def invite() {
  t = +datetime.datetime.now()
  inviterIdArr = [
    "pVbNk9xIuI02DeRtwUiztA==",
    "s4UuZYFN6GW3jbg4x9Z8LA==",
    "Vf+kZwVHm4/P5/ZkyCY+DA==",
    "4y1yGPA4HCaFNCw8BZ6gsw=="
  ]
  inviterId = inviterIdArr[Math.floor((Math.random() * inviterIdArr.length))]
  options = {
    url: `https://api.m.jd.com/?t={t}`,
    body: `functionId=InviteFriendChangeAssertsService&body={json.dumps({"method":"attendInviteActivity","data":{"inviterPin":encodeURIComponent(inviterId),"channel":1,"token":"","frontendInitStatus":""}})}&referer=-1&eid=eidI9b2981202fsec83iRW1nTsOVzCocWda3YHPN471AY78%2FQBhYbXeWtdg%2F3TCtVTMrE1JjM8Sqt8f2TqF1Z5P%2FRPGlzA1dERP0Z5bLWdq5N5B2VbBO&aid=&client=ios&clientVersion=14.4.2&networkType=wifi&fp=-1&uuid=ab048084b47df24880613326feffdf7eee471488&osVersion=14.4.2&d_brand=iPhone&d_model=iPhone10,2&agent=-1&pageClickKey=-1&platform=3&lang=zh_CN&appid=market-task-h5&_t={t}`,
    headers: {
      "Host": "api.m.jd.com",
      "Accept": "application/json, text/plain, */*",
      "Content-type": "application/x-www-form-urlencoded",
      "Origin": "https://invite-reward.jd.com",
      "Accept-Language": "zh-CN,zh-Hans;q=0.9",
      "User-Agent": user_info.isNode() ? (process.env.JS_USER_AGENT ? process.env.JS_USER_AGENT : (require('./JS_USER_AGENTS').USER_AGENT)) : (user_info.getdata('JSUA') ? user_info.getdata('JSUA') : "'jdltapp;iPad;3.1.0;14.4;network/wifi;Mozilla/5.0 (iPad; CPU OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/1"),
      "Referer": 'https://invite-reward.jd.com/',
      "Accept-Encoding": "gzip, deflate, br",
      "Cookie": cookie
    }
  }
  user_info.post(options, 
    //print(data)
  })
}

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
    "User-Agent": "jdapp;iPhone;9.4.4;14.3;network/4g;Mozilla/5.0 (iPhone; CPU iPhone OS 14_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/1")
  resp = requests.post(url_str, headers=headers)
  try:
    content = resp.content
    print(content)
    # if () {
    #   print(f'{json.dumps(err)}')
    #   print(f'{user_info.name} API请求失败，请检查网路重试')
    # else:
    if (content):
      data = json.loads(content)
      if data['retcode'] == 13:
        userInfo.isLogin = False  # cookie过期
        return

      if data['retcode'] == 0:
        userInfo.nickName = (data['base'] & data['base'].nickname) | | userInfo.UserName;
      else:
        userInfo.nickName = userInfo.UserName
    else:
      print('京东服务器返回空数据')
  except Exception as e:
    logging.exception(e)



def jsonParse(str) {
  if (typeof str == "string") {
    try:
      return json.loads(str);
    except Exception as e:
      print(e);
      user_info.msg(user_info.name, '', '请勿随意在BoxJs输入框修改内容\n建议通过脚本去获取cookie')
      return [];
    }
  }
}