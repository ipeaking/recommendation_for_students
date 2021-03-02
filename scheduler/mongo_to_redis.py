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
# @Time    : 2020-08-22 10:57
# @Author  : Hongbo Huang
# @File    : mongo_to_redis.py
import pymongo
from dao import redis_db
from dao.mongo_db import MongoDB



class write_to_redis(object):
    def __init__(self):
        self._redis = redis_db.Redis()
        self.mongo = MongoDB(db='loginfo')
        # self.db_loginfo = self.mongo.db_loginfo
        # self.collection = self.db_loginfo['content_labels']
        self.collection = self.mongo.db_client['content_labels']

    def get_from_mongoDB(self):
        '''
        创建管道,通过管道运输数据
        '''
        pipelines = [{
            '$group':{
                '_id': "$type"
            }
        }]

        types = self.collection.aggregate(pipelines) # aggregate总数,合计
        count = 0
        for type in types:
            cx = {"type": type['_id']}
            data = self.collection.find(cx) # 数据库中查找这个id
            for info in data:
                result = dict()
                result['describe'] = str(info['describe'])
                result['type'] = str(info['type'])
                result['title'] = str(info['title'])
                result['news_date'] = str(info['news_date'])
                result['content_id'] = str(info['_id'])
                result['likes'] = info['likes'] # 本身是文字就不用转了
                result['read'] = info['read']
                result['hot_heat'] = info['hot_heat']
                result['collections'] = info['collections']
                # self._redis.redis.delete(str(info['_id']))
                self._redis.redis.set("news_detail:"+str(info['_id']), str(result)) # 新增键值对
                if count % 100 == 0:     # 每100条打印一次进度
                    print(count)
                count += 1


if __name__ == '__main__':
    write_to_redis = write_to_redis()
    write_to_redis.get_from_mongoDB()
