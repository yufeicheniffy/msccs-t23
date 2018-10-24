import pymongo

class MongoCollection:

    def __init__(self,collectionname='func_test',databasename='Helpme',MongoURI="mongodb://Admin_1:glasgowcom@cluster0-shard-00-00-0yvu9.gcp.mongodb.net:27017,cluster0-shard-00-01-0yvu9.gcp.mongodb.net:27017,cluster0-shard-00-02-0yvu9.gcp.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true"):
        #connect to specific database
        # collections: Test;Train;Tweets; default:func_test to test
        try:
            self.client = pymongo.MongoClient(MongoURI)
            print("connected to client:" + repr(self.client.list_database_names()))
            self.database = self.client[databasename]
            self.collection = self.database[collectionname]
        except pymongo.errors.ConnectionFailure:
            print("failed to connect")

    def insert(self, item):
        try:
            self.collection.insert(item)
        except Exception as e:
            print("Error", e)

    def find_all(self):
        try:
            x = self.collection.find()
        except Exception as e:
            print("Error", e)
        return x

    def print_all(self):
        for e in self.find_all():
            print(e)

    def find_category_by_id(self, id):
        try:
            x = self.collection.find_one({"postID": str(id)})
        except Exception as e:
            print("Error", e)
        return x["categories"]

    def return_ids_list(self):
        l=[]
        all = self.find_all()
        for e in all:
            l.append(e["postID"])
        return l