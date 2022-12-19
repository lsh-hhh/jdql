# 用户信息
import json
import time


class UserInfo(object):
  def __init__(self):
    self.UserName = None
    self.score = 0
    self.name = ''
    self.total = 0
    self.index = 0
    self.nickName = 0
    self.isLogin = False
    self.taskName = ''
    self.log = ''

  def wait(self, param):
    time.sleep(1)

  def msg(self, user_name, message, url, body):
    print("%s%s\n%s%s" % user_name % message % url % json.dumps(body))

  def log(self, param, message):
    self.log += message

  def done(self):
    print(self.log)
