#!/usr/bin/env python 
# -*- coding: utf-8 -*-
#                       _oo0oo_
#                      o8888888o
#                      88" . "88
#                      (| -_- |)
#                      0\  =  /0
#                    ___/`---'\___
#                  .' \\|     |// '.
#                 / \\|||  :  |||// \
#                / _||||| -:- |||||- \
#               |   | \\\  -  /// |   |
#               | \_|  ''\---/''  |_/ |
#               \  .-\__  '-'  ___/-. /
#             ___'. .'  /--.--\  `. .'___
#          ."" '<  `.___\_<|>_/___.' >' "".
#         | | :  `- \`.;`\ _ /`;.`/ - ` : | |
#         \  \ `_.   \_ __\ /__ _/   .-` /  /
#     =====`-.____`.___ \_____/___.-`___.-'=====
#                       `=---='
#
#
#     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#               佛祖保佑         永无BUG
# @Time    : 2020-08-22 10:13
# @Author  : Hongbo Huang
# @File    : mysql_db.py
import sys
sys.path.append('..')
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base



'''
declarative_base类维持了一个从类到表的关系，通常一个应用使用一个base实例，所有实体类都应该继承此类对象

mysql创建数据库的引擎,创建会话
_就是私有化方法
'''
class Mysql(object):
    def __init__(self):
        Base = declarative_base()
        self.engine = create_engine("mysql+pymysql://root:123456@47.104.154.74:3306/sina", encoding='utf-8')
        self._DBSession = sessionmaker(bind=self.engine)

