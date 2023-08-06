# -*- coding: utf-8 -*-
# @Time : 2022/3/9 1:33 下午
# @Author : chendb
# @Description : 工具集合


import yagmail
import json
import requests
from loguru import logger

def json_util(pre_json, to_json_type, **kwargs):
    """
    json解析
    :param pre_json:
    :param to_json_type:
    :param kwargs:
    :return:
    """
    try:
        return json.loads(pre_json) if to_json_type == 'json_load' else json.dumps(
            pre_json, ensure_ascii=False, **kwargs)
    except:
        return pre_json

def http_client_util(url, method, data, **kwargs):
    up_method = method.upper()
    if up_method == 'POST':
        res = requests.post(url, data=data, **kwargs)
    elif up_method == 'PUT':
        res = requests.put(url, data=data)
    elif up_method == 'DELETE':
        res = requests.delete(url, data=data, **kwargs)
    elif up_method == 'OPTIONS':
        res = requests.options(url, **kwargs)
    elif up_method == 'HEAD':
        res = requests.head(url, **kwargs)
    elif up_method == 'PATCH':
        res = requests.patch(url, data=data, **kwargs)
    else:
        res = requests.get(url, params=data, **kwargs)
    res.encoding = 'utf-8'
    return res

def trans_data_to_url_util(url, data):
    """
    参数转成url形式展示拼接
    :param url:
    :param data:
    :return:
    """
    if data:
        url = f'{url}?{"&".join([f"{k}={v}" for k, v in data.items()])}'
    return url

def send_mail_util(from_user, pwd, host, to_user, subject, content):
    """
    发送邮件
    :param from_user: 发件人
    :param pwd: 密码
    :param host: 发件地址host
    :param to_user: 接收人
    :param subject: 邮件主题
    :param content: 邮件内容
    :return:
    """
    with yagmail.SMTP(user=from_user, password=pwd, host=host) as yag:
        yag.send(to_user, subject, content)

def send_robot_msg_util(msg, at_all, qy_wechat_token=''):
    """
    企业微信机器人 webhook
    :param msg:
    :param send_type:
    :param at_all:
    :param qy_wechat_token:
    :return:
    """
    payloads = {"msgtype": "text", "text": {"content": msg}}
    payloads['text']['mentioned_mobile_list'] = ['@all'] if at_all is True else at_all
    url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send'
    pre_data = {'key': qy_wechat_token}
    url = trans_data_to_url_util(url, pre_data)
    data = json_util(payloads, 'json_dump').encode('utf-8')
    http_client_util(url, 'POST', data=data, headers={'Content-Type': 'application/json'})

def logger_util(msg):
    """
    记录日志
    :param msg:
    :return:
    """
    logger.info(f'\n{msg}')

if __name__ == '__main__':
    logger_util('日志记录!!!')
#     send_robot_msg_util(msg = '线上配置走查', at_all=['@all'], qy_wechat_token= '7fdda192-cfcb-4eb5-87a5-b341574562d5')
