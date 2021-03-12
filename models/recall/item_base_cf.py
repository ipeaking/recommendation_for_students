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
# @Time    : 2020-10-13 20:36
# @Author  : Hongbo Huang
# @File    : item_base_cf.py
from tqdm import tqdm
import math


class ItemBaseCF(object):
    def __init__(self, train_file):
        '''
        读取文件,用户和item的历史, item的相似度,训练
        '''
        self.train = dict()
        self.user_item_history = dict()
        self.item_to_item = dict()
        self.read_data(train_file)

    def read_data(self, train_file):
        """
            读文件，并生成数据集（用户、分数、新闻user,score,item）
            :param train_file: 训练文件
            :return: {person_id:{content_id:predict_score}}
        """
        with open(train_file, mode='r', encoding='utf-8') as rf:
            for line in tqdm(rf.readlines()):
                user, score, item = line.strip().split(",")
                self.train.setdefault(user, {}) # 训练只是训练用户的
                self.user_item_history.setdefault(user, {})
                self.train[user][item] = int(score) # 用户,item的分数
                self.user_item_history[user].append(item) # 历史记录才需要添加item

    def cf_item_train(self):
        """
        基于item的协同过滤，计算相似度
        :return:  相似度矩阵{content_id:{content_id: 相似度得分}}
        """
        self.item_to_item, self.item_count = dict(), dict()  # 文章-文章的共现矩阵，文章被多少个用户阅读
        for user, items in self.train.items():
            for i in items.keys:
                self.item_count.setdefault(i, 0)
                self.item_count[i] += 1  # item i出现一次我就加上1

        for user, items in self.train.items():
            for i in items.keys:
                self.item_to_item.setdefault(i, {})
                for j in items.keys():
                    if i == j:
                        continue
                    self.item_to_item[i].setdefault(i, {})
                    self.item_to_item[i][j] += 1 / (math.sqrt(self.item_count[i] * self.item_count[j])) # item i 和 j 共现一次就加1

        # 计算相似度矩阵
        for _item in self.item_to_item:
            self.item_to_item[_item] = dict(sorted(self.item_to_item[_item].items(),
                                            key=lambda x: x[1], reverse=True)[0:50])   # reverse就是倒序


    # TODO 保存算法模型
    def save_variable(self):
        return

    def cal_rec_item(self, user, N=50):
        """
        给用户user推荐前N个感兴趣的文章
        :param user:
        :param W:
        :param K:
        :return: 推荐文章的列表
        """
        rank = dict()  # 记录user的推荐文章（没有历史行为的文章） 和 感兴趣程度
        try:
            action_item = self.train[user] # 之前发生训练过的文章
            for item, score in action_item.items():
                for j, wj in self.item_to_item[item].items():  # 之前训练的文章列表
                    if j in action_item.keys():   # 如果文章j已经被阅读过了，那么我们就不推荐
                        continue
                    rank.setdefault(j, 0)
                    rank[j] += score * wj / 1000 # 如果文章j没有被购买过，则累计文章j与item的相似度*兴趣评分，作为user对文章j的兴趣度
            res = dict(sorted(rank.items(), key=lambda x: x[1], reverse=True)[0:N])
            return list(res)
        except:
            return {}
