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
# @Time    : 2020-10-13 20:56
# @Author  : Hongbo Huang
# @File    : sched_rec_news.py
from read_data import read_news_data
from models.recall import item_base_cf


class SchedRecNews(object):
    def __init__(self):
        self.new_data = read_news_data.NewsData()
        return

    def schedule_job(self):
        # TODO 1.计算得分  2.训练模型   3.做推荐   4.把推荐的结果存入到数据库里
        # 要计算得分，首先我们要知道给谁计算得分，也就是说我们要知道推荐用户的列表， 分成冷启动和有推荐列表的， 我们只需要给有推荐列表的人去计算
        # 也就是说，什么样的人有推荐列表呢？ 一定是使用过我们的App的，所以我们暂时认为一定是有阅读记录的人
        # 所以我们在这里，就要把有阅读记录的人拿出来
        user_list = self.new_data.rec_users()



    def cal_score(self, user_set):
        return

    def rec_list(self, user_id):
        # TODO 把用户传进来，然后调用模型预测这个用户的推荐列表
        return

    def to_redis(self, user_id, rec_content_score):
        return


if __name__ == '__main__':
    sched = SchedRecNews()
    sched.schedule_job()