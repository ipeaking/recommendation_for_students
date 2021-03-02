import pymongo
import datetime


'''
mongoDB数据库连接,客户端,数据库
'''
class MongoDB(object):
    def __init__(self, db):
        mongo_client = self._connect('47.104.154.74', 27017, '', '', db) # 另外2个是用户名,密码
        self.db_client = mongo_client[db]    # 数据库
        self.collection_test = self.db_client['test_collections'] # 数据表
        return

    def _connect(self, host, port, user, pwd, db):
        mongo_info = self._splicing(host, port, user, pwd, db) # 拼接字符
        mongo_client = pymongo.MongoClient(mongo_info, connectTimeoutMS=12000, connect=False)  #一定要注意哦
        return mongo_client

    @staticmethod
    def _splicing(host, port, user, pwd, db):
        client = 'mongodb://' + host + ":" + str(port) + "/"
        if user != '':
            client = 'mongodb://' + user + ":" + pwd + "@" + host + ":" + str(port) + "/"
            if db != '':
                client += db
        return client

    def test_insert(self):
        testcollection = dict()
        testcollection['name'] = '黄鸿波'
        testcollection['job'] = 'programmer'
        testcollection['dates'] = datetime.datetime.utcnow()
        self.collection_test.insert_one(testcollection)

if __name__ == '__main__':
    mongo = MongoDB(db='loginfo')
    mongo.test_insert()