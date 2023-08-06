# -*- coding: utf-8 -*-
# @Time : 2022/3/9 1:33 下午
# @Author : chendb
# @Description : 工具集合


import yagmail
import time
import hashlib
import hmac
import base64
import urllib.parse
import json
import requests


def time_stamp_util(time_type):
    """
    时间戳相关
    :param time_type:
    :return:
    """
    t = time.time()
    stamp = int(t * 1000) if time_type == 'ms' else int(t)
    return stamp

def to_encrypt_util(pre_str, en_type, sign_key=''):
    """
    加密相关
    :param pre_str:
    :param en_type:
    :param sign_key:
    :return:
    """
    if en_type == 'sha_256':
        return hashlib.sha256(pre_str.encode('utf-8')).hexdigest()
    elif en_type == 'md5':
        md5 = hashlib.md5(sign_key.encode('utf-8'))
        md5.update(pre_str.encode('utf-8'))
        return md5.hexdigest()
    elif en_type == 'hmac_256':
        return hmac.new(sign_key.encode("utf-8"), pre_str.encode("utf-8"), digestmod=hashlib.sha256).digest()
    else:
        return pre_str

def string_coding_util(pre_str, string_coding_type):
    """
    编码解码相关
    :param pre_str:
    :param string_coding_type:
    :return:
    """
    if string_coding_type == 'url_encode':
        return urllib.parse.quote_plus(pre_str)
    elif string_coding_type == 'url_decode':
        return urllib.parse.unquote(pre_str)
    elif string_coding_type == 'base_64_encode':
        return base64.b64encode(pre_str)
    else:
        return pre_str

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
    get类型的参数转成url形式展示拼接
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

# def send_robot_msg_util(msg, send_type, at_all, ding_talk_sign_key='', ding_talk_token='', qy_wechat_token=''):
#     payloads = {"msgtype": "text", "text": {"content": msg}}
#     if send_type == 'dingTalk':
#         payloads['at'] = {'isAtAll': True, 'atMobiles': []} \
#             if at_all is True else {'atMobiles': at_all, 'isAtAll': False}
#         url = 'https://oapi.dingtalk.com/robot/send'
#         time_stamp = time_stamp_util('ms')
#         pre_str = f'{time_stamp}\n{ding_talk_sign_key}'
#         hmac_256_str = to_encrypt_util(pre_str, 'hmac_256', ding_talk_sign_key)
#         base_64_str = string_coding_util(hmac_256_str, 'base_64_encode')
#         sign = string_coding_util(base_64_str, 'url_encode')
#         pre_data = {'access_token': ding_talk_token, 'timestamp': time_stamp, 'sign': sign}
#     else:
#         payloads['text']['mentioned_mobile_list'] = ['@all'] if at_all is True else at_all
#         url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send'
#         pre_data = {'key': qy_wechat_token}
#     url = trans_data_to_url_util(url, pre_data)
#     data = json_util(payloads, 'json_dump').encode('utf-8')
#     http_client_util(url, 'POST', data=data, headers={'Content-Type': 'application/json'})

def send_robot_msg_util(msg, send_type, at_all, qy_wechat_token=''):
    payloads = {"msgtype": "text", "text": {"content": msg}}
    payloads['text']['mentioned_mobile_list'] = ['@all'] if at_all is True else at_all
    url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send'
    pre_data = {'key': qy_wechat_token}
    url = trans_data_to_url_util(url, pre_data)
    data = json_util(payloads, 'json_dump').encode('utf-8')
    http_client_util(url, 'POST', data=data, headers={'Content-Type': 'application/json'})
