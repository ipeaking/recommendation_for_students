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
        self.seg = Segment(stopword_files=[], userdict_files=[])
        self.engine = Mysql()
        self.session = self.engine._DBSession()  #构建session
        self.mongo = MongoDB(db='recommendation')
        self.db_loginfo = self.mongo.db_loginfo    #数据库
        self.collection = self.db_loginfo['content_labels']   #使用集合

    def get_data_from_mysql(self):
        types = self.session.query(distinct(Content.type))   #distinct查询不同的类型
        for i in types:
            print(i[0])
            res = self.session.query(Content).filter(Content.type == i[0])
            if res.count() > 0:
                for x in res.all():
                    keywords = self.get_keywords(x.content, 10)
                    word_nums = self.get_words_nums(x.content)
                    times = x.time
                    create_time = datetime.utcnow()    #使用utc时间
                    content_collection = dict()
                    content_collection['describe'] = x.content
                    content_collection['keywords'] = keywords
                    content_collection['word_num'] = word_nums
                    content_collection['news_date'] = times
                    content_collection['hot_heat'] = 10000
                    content_collection['type'] = x.type
                    content_collection['title'] = x.title
                    content_collection['likes'] = 0
                    content_collection['read'] = 0
                    content_collection['collections'] = 0
                    content_collection['create_time'] = create_time
                    self.collection.insert_one(content_collection)

            self.session.query(Content).filter(Content.type == i[0]).delete()

    def get_keywords(self, contents, nums=10):
        keywords = self.seg.extract_keyword(contents)[:nums]
        return keywords

    def get_words_nums(self, contents):
        ch = re.findall('([\u4e00-\u9fa5])', contents)    #判断中文的字符编码
        nums = len(ch)
        return nums


if __name__ == '__main__':
    content_label = ContentLabel()
    content_label.get_data_from_mysql()