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
# @Time    : 2020-11-11 20:38
# @Author  : Hongbo Huang
# @File    : YoutubeDNN.py
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from models.recall.preprocess import gen_data_set, gen_model_input


class YoutubeDNN(object):
    def __init__(self, embedding_dim=32):
        self.SEQ_LEN = 50  # 最长点击item的数量
        self.embedding_dim = embedding_dim
        self.user_feature_columns = None
        self.item_feature_columns = None

    def training_set_construct(self):
        # 加载数据
        data = pd.read_csv('../../data/read_history.csv')
        # 负采样的个数
        negsample = 0
        # 特征编码
        features = ['user_id', 'item_id', 'gender', 'age', 'city']
        feature_max_idx = {}
        for feature in features:
            lbe = LabelEncoder()
            data[feature] = lbe.fit_transform(data[feature]) + 1
            feature_max_idx[feature] = data[feature].max() + 1
        # 抽取用户、物品特征
        user_info = data[["user_id", "gender", "age", "city"]].drop_duplicates('user_id')
        item_info = data[["item_id"]].drop_duplicates('item_id')
        user_info.set_index("user_id", inplace=True)

        # 构建输入数据
        train_set, test_set = gen_data_set(data, negsample)
        # 转化为模型的输入
        train_model_input, train_label = gen_model_input(train_set, user_info, self.SEQ_LEN)
        test_model_input, test_label = gen_model_input(test_set, user_info, self.SEQ_LEN)

        # 用户端的特征输入
        # 物品端的特征输入
        return True

    def training_model(self):
        return

    def extract_embedding_layer(self):
        return

    def eval(self):
        return

    def scheduler(self):
        # 构建训练集、测试集

        # 训练模型

        # 获取用户、item的layer

        # 评估模型

        return True