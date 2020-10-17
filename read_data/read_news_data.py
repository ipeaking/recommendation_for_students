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
# @Time    : 2020-10-17 10:57
# @Author  : Hongbo Huang
# @File    : read_news_data.py
from dao.mongo_db import MongoDB
import os


class NewsData(object):
    def __init__(self):
        self.mongo = MongoDB(db='loginfo')
        self.db_client = self.mongo.db_client
        self.read_collection = self.db_client['read']

    """
        #TODO 作业
        点赞   2分
        收藏   3分
        阅读   1分
        如果同时存在2项  加 1分 
        如果同时存在3项  加 2分
    """
    def get_data(self):
        result = list()
        data = self.read_collection.find()
        for info in data:
            result.append(str(info['user_id']) + ',1,' + str(info['content_id']))
        self.to_csv(result, '../data/news_score/news_log.csv')

    def rec_users(self):
        data = self.read_collection.distinct('user_id')
        return data

    def to_csv(self, user_score_content, res_file):
        if not os.path.exists('../data/news_score'):
            os.mkdir('../data/news_score')
        with open(res_file, mode='w', encoding='utf-8') as wf:
            for info in user_score_content:
                wf.write(info + '\n')
        print(len(user_score_content))


if __name__ == '__main__':
    news_data = NewsData()
    news_data.rec_users()


