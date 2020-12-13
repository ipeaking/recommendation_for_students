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
# @Time    : 2020-11-25 20:52
# @Author  : Hongbo Huang
# @File    : user_short_label.py
from dao.mongo_db import MongoDB
from bson.objectid import ObjectId
import collections


class UserShortLabel(object):
    """
    1、拿到每个用户每一天读的内容，取用户id+content_id+时间
    2、从第一步中拿出每一天的数据，然后取相关的用户特征，并进行累加
    3、形成每个用户每一天的用户画像，即短期用户画像

    """
    def __init__(self):
        self.mongo = MongoDB(db='loginfo')
        self.db_loginfo = self.mongo.db_client  # 数据库
        # self.collection = self.db_loginfo['read']  # 使用集合
        self.collection = self.mongo.collection_read
        self.content_info = self.mongo.collection_content
        self.user_short_label = self.mongo.user_short_label

    # 拿到用户每一天读的内容
    # def get_data(self):
    #     data = self.collection.find()
    #     for info in data:
    #         # print(info['content_id'])
    #         # print(info['user_id'], info['content_id'], info['date'])
    #         self.get_read_info(info['content_id'])

    def get_read_info(self):
        result = dict()
        # 每一个content_ids 就相当于是一个用户一天的阅读记录
        content_ids = ["5fa359820574d6367aaf1a53", "5fa359820574d6367aaf1a53", "5fa359830574d6367aaf1a56"]
        # content_id = "5fa359820574d6367aaf1a53"
        result_lst = list()
        result_type_list = list()
        for content_id in content_ids:
            find_collection = {"_id": ObjectId(content_id)}
            content = self.content_info.find(find_collection)
            for info in content:
                for i in info["keywords"]:
                    result_lst.append(i[0])

        # print(result_type_list)

        print(self.total_kw([result_lst]))
        result['user_id'] = 255
        result['short_kw'] = self.total_kw([result_lst])
        # result['log_time'] =
        # result['type_num'] = 每一天阅读的内容所涉及到的类型的总数
        self.user_short_label.insert(result)


    #关键字的累加
    def total_kw(self, kw_list):
        lst = []
        for i in kw_list:
            for j in i:
                lst.append(str(j))
        result = collections.Counter(lst)

        return result


if __name__ == '__main__':
    user_short_data = UserShortLabel()
    user_short_data.get_read_info()