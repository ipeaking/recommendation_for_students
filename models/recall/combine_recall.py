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
# @Time    : 2020-10-28 21:11
# @Author  : Hongbo Huang
# @File    : combine_recall.py
import pickle
from models.recall.lfm_recall import LFM_model
from config import params
from util import log_utils

logger = log_utils.Logger()


class CombineRecallTrain(object):

    def __init__(self):
        self.model_train()
        self.predict('224')
        self.save_to_redis()

    def model_train(self):
         """
         训练联合模型，hot_recall，itemCF，LFM
         """
         self.LFM_train()
         self.CF_train()
         self.NMF_train()

    def LFM_train(self):
         logger.info("start train LFM model")
         news_model_train = LFM_model(params.NEWS_SCORE)
         news_model_train.lfm_train()
         logger.info("end train LFM model")
         with open("LFMmodel.pkl", mode="wb") as news_f:
             pickle.dumps(news_model_train)

    def predict(self, user_id):
         news_model_train = LFM_model(params.NEWS_SCORE)
         news_model_train.lfm_train()
         result_recall = news_model_train.model_predict(user_id)
         return result_recall

    def save_to_redis(self):
        return


if __name__ == '__main__':
    cr = CombineRecallTrain()
    cr.LFM_train()