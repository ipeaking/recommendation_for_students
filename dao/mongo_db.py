import pymongo
import datetime

class MongoDB(object):
    def __init__(self, db):
        mongo_client = self._connect('47.104.154.74', 27017, '', '', db)
        self.db_loginfo = mongo_client['loginfo']
        self.collection_test = self.db_loginfo['test_collections']
        return

    def _connect(self, host, port, user, pwd, db):
        mongo_info = self._splicing(host, port, user, pwd, db)
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
    mongo = MongoDB(db='test')
    mongo.test_insert()