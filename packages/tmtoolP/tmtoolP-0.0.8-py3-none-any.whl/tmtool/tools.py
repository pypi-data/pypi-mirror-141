# -*- coding: utf-8 -*-
# @Time : 2022/3/9 1:39 下午
# @Author : chendb
# @Description :

from .util import send_mail_util, send_robot_msg_util


class Tool(object):


    def __init__(self):
        self.mail_from_user = ''    # 邮件发送者账号
        self.mail_from_user_pwd = ''    # 邮件发送者密码
        self.mail_from_user_host = ''    # 邮件发送者host
        self.qy_wechat_token = ''  # 企业微信机器人token

    def send_mail_msg(self, to_user, subject, content):
        send_mail_util(self.mail_from_user, self.mail_from_user_pwd, self.mail_from_user_host, to_user, subject, content)

    def send_qy_wechat_msg(self, msg, at_all=None):
        # 发送企业微信webhook
        if at_all is None:
            at_all = []
        send_robot_msg_util(msg, 'qyWechat', qy_wechat_token=self.qy_wechat_token, at_all=at_all)

