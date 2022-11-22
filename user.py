# 用户信息
import time


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
