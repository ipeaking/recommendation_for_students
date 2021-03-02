#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from datetime import datetime
from dao.mongo_db import MongoDB
from dao.mysql_db import Mysql
from models.keywords.tfidf import Segment
from sqlalchemy import distinct
from models.labels.entity.content import Content


class ContentLabel(object):
    def __init__(self):
        self.seg = Segment(stopword_files=[], userdict_files=[]) # 划分

        self.engine = Mysql()
        self.session = self.engine._DBSession()

        self.mongo = MongoDB(db='recommendation')
        # self.db_loginfo = self.mongo.db_loginfo
        # self.collection = self.db_loginfo['content_labels']
        self.collection = self.mongo.db_client['content_labels'] # 客服端连接

    def get_data_from_mysql(self):
        types = self.session.query(distinct(Content.type)) # distinct不同种类的   文本类型
        for i in types:
            print(i[0])
            res = self.session.query(Content).filter(Content.type == i[0])
            if res.count() > 0:
                for x in res.all():
                    keywords = self.get_keywords(x.content, 10) # 设定关键词的数量
                    word_nums = self.get_words_nums(x.content)
                    times = x.time # 文本的时间
                    create_time = datetime.utcnow()
                    content_collection = dict()
                    content_collection['describe'] = x.content # 文本的内容
                    content_collection['keywords'] = keywords
                    content_collection['word_num'] = word_nums
                    content_collection['news_date'] = times
                    content_collection['hot_heat'] = 10000
                    content_collection['type'] = x.type # 文本的类型
                    content_collection['title'] = x.title # 文本的标题
                    content_collection['likes'] = 0
                    content_collection['read'] = 0
                    content_collection['collections'] = 0
                    content_collection['create_time'] = create_time
                    self.collection.insert_one(content_collection)

    def get_keywords(self, contents, nums=10):
        keywords = self.seg.extract_keyword(contents)[:nums] #  extract提取
        return keywords

    def get_words_nums(self, contents):
        ch = re.findall('([\u4e00-\u9fa5])', contents) # \u4e00-\u9fa5  Unicode编码判断是否为中文
        nums = len(ch)
        return nums


if __name__ == '__main__':
    content_label = ContentLabel()
    content_label.get_data_from_mysql()
