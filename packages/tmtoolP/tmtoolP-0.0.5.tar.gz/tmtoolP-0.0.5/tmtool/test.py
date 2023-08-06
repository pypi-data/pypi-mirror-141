# -*- coding: utf-8 -*-
# @Time : 2022/3/10 11:14 上午
# @Author : chendb
# @Description : 测试

from tmtool.tools import Tool

tool = Tool()

tool.qy_wechat_token = '7fdda192-cfcb-4eb5-87a5-b341574562d5'
# @所有人
tool.send_qy_wechat_msg('线上配置走查', at_all=['@all'])
# # @指定单人
# tool.send_qy_wechat_msg('线上配置走查', at_all=['18600967174'])
# # @指定多人
# tool.send_qy_wechat_msg('线上配置走查', at_all=['15210205078', '18701105997', '13821910557', '13426002048'])


