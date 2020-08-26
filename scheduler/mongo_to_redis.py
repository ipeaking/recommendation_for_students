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
        self.db_loginfo = self.mongo.db_loginfo
        self.collection = self.db_loginfo['content_labels']

    def get_from_mongoDB(self):
        pipelines = [{
            '$group':{
                '_id': "$type"
            }
        }]

        types = self.collection.aggregate(pipelines)
        count = 0
        for type in types:
            cx = {"type": type['_id']}
            data = self.collection.find(cx)
            for info in data:
                result = dict()
                result['describe'] = info['describe']
                result['type'] = info['type']
                result['news_date'] = info['news_date']
                # self._redis.redis.delete(str(info['_id']))
                self._redis.redis.set("news_detail:"+str(info['_id']), str(result))
                if count % 100 == 0:
                    print(count)
                count += 0


if __name__ == '__main__':
    write_to_redis = write_to_redis()
    write_to_redis.get_from_mongoDB()
