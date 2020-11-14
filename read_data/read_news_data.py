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
import time


class NewsData(object):
    def __init__(self):
        self.mongo = MongoDB(db='loginfo')
        self.db_client = self.mongo.db_client     #数据库的客户端
        self.read_collection = self.db_client['read']
        self.likes_collection = self.db_client['likes']
        self.collection = self.db_client['collections']
        self.content = self.db_client['content_labels']

    def test_content_time(self):
        t = time.time()
        data = self.content.find({"collections": 0}, {"collections": 1})

        for info in data:
            print(info)

        print(time.time() - t)       #打印消耗的时间

    """
        #TODO 作业
        点赞   2分
        收藏   3分
        阅读   1分
        如果同时存在2项  加 1分 
        如果同时存在3项  加 2分
    """
    def cal_score(self):
        result = list()
        score_dict = dict()
        data = self.read_collection.find()
        for info in data:
            if score_dict.get(info['user_id']) and score_dict[info['user_id']].get(info['content_id']):
                print("user_id : {} ,content_id : {} is exist".format(info['user_id'], info['content_id']))
                continue
            score_dict.setdefault(info['user_id'], {})
            score_dict[info['user_id']].setdefault(info['content_id'], 0)

            query = {"user_id": info['user_id'], "content_id": info['content_id']}

            exist_count = 0

            read_count = self.read_collection.find(query).count()
            if read_count > 0:
                score_dict[info['user_id']][info['content_id']] += 1
                exist_count += 1

            like_count = self.likes_collection.find(query).count()
            if like_count > 0:
                score_dict[info['user_id']][info['content_id']] += 2
                exist_count += 1
            collection_count = self.collection.find(query).count()

            if collection_count > 0:
                score_dict[info['user_id']][info['content_id']] += 3
                exist_count += 1

            if exist_count == 2:
                score_dict[info['user_id']][info['content_id']] += 1
            elif exist_count == 3:
                score_dict[info['user_id']][info['content_id']] += 2
            else:
                pass

            result.append(str(info['user_id']) + ',' + str(score_dict[info['user_id']][info['content_id']]) + ',' + str(info['content_id']))
        self.to_csv(result, '../data/news_score/result_score.csv')     

    def rec_users(self):
        data = self.read_collection.distinct('user_id')   #不同的用户,去掉相同的召回用户
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
    news_data.cal_score()


