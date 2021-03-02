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
# @Time    : 2020-08-22 11:18
# @Author  : Hongbo Huang
# @File    : simple_rec.py
from dao import redis_db
from dao.mongo_db import MongoDB


class SimpleRecList(object):
    def __init__(self):
        self._redis = redis_db.Redis()
        self.mongo = MongoDB(db='recommendation')
        # self.db_loginfo = self.mongo.db_loginfo
        # self.collection = self.db_loginfo['content_labels']
        self.collection = self.mongo.db_client['content_labels']

    def get_news_order_by_time(self):
        data = self.collection.find().sort([{"$news_date", -1}]) # 根据时间倒序排序,可以有多个排序,所以是列表
        count = 10000

        '''
        Redis Zadd 命令用于将一个或多个成员元素及其分数值加入到有序集当中。
        如果某个成员已经是有序集的成员，那么更新这个成员的分数值，并通过重新插入这个成员元素，来保证该成员在正确的位置上。
        分数值可以是整数值或双精度浮点数。
        如果有序集合 key 不存在，则创建一个空的有序集并执行 ZADD 操作。
        当 key 存在但不是有序集类型时，返回一个错误
        '''

        for news in data:
            self._redis.redis.zadd("rec_list", {str(news['_id']): count}) # redis.zadd,只是更新成员的顺序,比如前10000名成员的顺序
            count -= 1
            if count % 10 == 0:
                print(count)


if __name__ == '__main__':
    simple = SimpleRecList()
    simple.get_news_order_by_time()