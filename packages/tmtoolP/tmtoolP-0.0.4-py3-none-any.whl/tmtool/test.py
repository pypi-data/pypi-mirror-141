# -*- coding: utf-8 -*-
# @Time : 2022/3/10 11:14 上午
# @Author : chendb
# @Description : 测试

from tmtool.tools import Tool

tool = Tool()

tool.qy_wechat_token = '7fdda192-cfcb-4eb5-87a5-b341574562d5'
tool.send_qy_wechat_msg('线上配置走查')
