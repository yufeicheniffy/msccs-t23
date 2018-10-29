import pymongo
import numpy as np
from HelpMeTokenizer import HelpMeTokenizer

class MongoCollection:
    catadictionary={'GoodsServices':0, 'SearchAndRescue':1,'InformationWanted':2,'Volunteer':3,'Donations':4,
                    'MovePeople':5, 'FirstPartyObservation': 6, 'ThirdPartyObservation': 7, 'Weather': 8, 'EmergingThreats': 9,
                    'SignificantEventChange':10, 'MultimediaShare': 11, 'ServiceAvailable': 12, 'Factoid': 13, 'Official': 14,
                    'CleanUp':15, 'Hashtags': 16, 'PastNews': 17, 'ContinuingNews': 18, 'Advice': 19,
                    'Sentiment':20, 'Discussion': 21, 'Irrelevant': 22, 'Unknown': 23, 'KnownAlready': 24,
                    }
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

    def find_category_by_id(self, postid):
        try:
            x = self.collection.find_one({"postID": str(postid)})
        except Exception as e:
            print("Error", e)
        return x["categories"]

    def find_text_by_id(self,postid):
        try:
            x = self.collection.find_one({"identifier": str(postid)})
            if (x is None):
                x = self.collection.find_one({"postID": str(postid)})
        except Exception as e:
            print("Error", e)
        return x["text"]

    def return_ids_list(self):
        l=[]
        all = self.find_all()
        for e in all:
            l.append(e["postID"])
        return l

    def return_catmatrix_by_id(self, postid):
        try:
            catmatrix=np.full((25,), 0)
            catalist=self.find_category_by_id(postid)
            for e in catalist:
                i=self.catadictionary.get(e)
                catmatrix[i]=1
        except Exception as e:
            print("Error", e)
        return catmatrix

    def return_tokenizers_by_id(self,postid):
        try:
         token=HelpMeTokenizer()
        except Exception as e:
            print("Error", e)
        return token.process(self.find_text_by_id(postid))

    def return_train_dic(self):
        try:
            dic={}
            for e in self.return_ids_list():
                dic.setdefault(e,[]).append([self.return_catmatrix_by_id(e),self.return_tokenizers_by_id(e)])
        except Exception as e:
            print("Error", e)
        return dic
