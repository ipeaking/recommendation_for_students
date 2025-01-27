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
# @Time    : 2020-08-22 10:31
# @Author  : Hongbo Huang
# @File    : content.py
from sqlalchemy import Column,Integer,DateTime,Text
from sqlalchemy.ext.declarative import declarative_base      #自己导入
Base = declarative_base()
from dao.mysql_db import Mysql

class Content(Base):              
    '''
    表名, 字段
    '''
    __tablename__ = 'data'       
    id = Column(Integer(), primary_key=True)
    time = Column(DateTime())
    title = Column(Text())
    content = Column(Text())
    type = Column(Text())

    def __init__(self):
        mysql = Mysql()
        engine = mysql.engine
        Base.metadata.create_all(engine)   # 创建所有的引擎