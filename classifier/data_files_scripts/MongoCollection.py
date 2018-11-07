import sys
sys.path.insert(0, './data_files_scripts')

import pymongo
import numpy as np

class MongoCollection:
    catadictionary={'GoodsServices':0, 'SearchAndRescue':1,'InformationWanted':2,'Volunteer':3,'Donations':4,
                    'MovePeople':5, 'FirstPartyObservation': 6, 'ThirdPartyObservation': 7, 'Weather': 8, 'EmergingThreats': 9,
                    'SignificantEventChange':10, 'MultimediaShare': 11, 'ServiceAvailable': 12, 'Factoid': 13, 'Official': 14,
                    'CleanUp':15, 'Hashtags': 16, 'PastNews': 17, 'ContinuingNews': 18, 'Advice': 19,
                    'Sentiment':20, 'Discussion': 21, 'Irrelevant': 22, 'Unknown': 23, 'KnownAlready': 24,
                    }
    #the dictionary to find the catagory index in catarogy array.
    def __init__(self,collectionname='func_test',databasename='Helpme',MongoURI="mongodb://Admin_1:glasgowcom@cluster0-shard-00-00-0yvu9.gcp.mongodb.net:27017,cluster0-shard-00-01-0yvu9.gcp.mongodb.net:27017,cluster0-shard-00-02-0yvu9.gcp.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true"):
        #connect to cloud database default. chage to local,set:  MongoURI="mongodb://localhost:27017/"
        #collections: Test;Train;Tweets; default:func_test to test
        try:
            self.client = pymongo.MongoClient(MongoURI)
            print("connected to client:" + repr(self.client.list_database_names()))
            self.database = self.client[databasename]
            self.collection = self.database[collectionname]
        except pymongo.errors.ConnectionFailure:
            print("failed to connect")

    def insert(self, item):
        """
        Insert the given item to the collection

        :param item: item to insert
        """
        try:
            self.collection.insert(item)
        except Exception as e:
            print("Error", e)

    def find_all(self):
        """
        Find all documents in the collection 

        :return: all documents
        """
        try:
            x = self.collection.find()
        except Exception as e:
            print("Error", e)
        return x

    def print_all(self):
        """
        Print all documents in the collection.
        """
        for e in self.find_all():
            print(e)

    def find_category_by_id(self, postid):
        """
        Lookup the category of the given tweet.

        :param postid: tweet to lookup
        :return: categories of tweet
        """
        try:
            x = self.collection.find_one({"postID": str(postid)})
        except Exception as e:
            print("Error", e)
        return x["categories"]

    def find_text_by_id(self,postid):
        """
        Lookup the text of the given tweet.

        :param postid: tweet to lookup
        :return: text of tweet
        """
        try:
            x = self.collection.find_one({"identifier": str(postid)})
            if (x is None):
                x = self.collection.find_one({"postID": str(postid)})
        except Exception as e:
            print("Error", e)
        return x["text"]

    def return_ids_list(self):
        """
        Return all tweet ids in collection.

        :return: list of tweet ids
        """
        l=[]
        all = self.find_all()
        for e in all:
            l.append(e["postID"])
        return l

    def return_catmatrix_by_id(self, postid):
        """
        ....
        """
        try:
            catmatrix=np.full((25,), 0)
            catalist=self.find_category_by_id(postid)
            for e in catalist:
                i=self.catadictionary.get(e)
                catmatrix[i]=1
        except Exception as e:
            print("Error", e)
        return catmatrix

    def return_catmatrix_all(self):
        """
        ....
        """
        try:
            idlist=self.return_ids_list()
            catmaxtrixAll=np.full((len(idlist),25),0)
            for i,id in zip(range(0,len(idlist)),idlist):
                catmaxtrixAll[i,:]=self.return_catmatrix_by_id(id)
        except Exception as e:
            print('Error',e)
        return catmaxtrixAll

    def create_catmatrix(self, categories):
        """
        Return a binary category array.
        """
        try:
            catmatrix=np.full((25,), 0)
            for e in categories:
                i=self.catadictionary.get(e)
                catmatrix[i]=1
        except Exception as e:
            print("Error", e)
        return catmatrix

    def return_catdict_all(self):
        """
        Return a dictionary of ID to list of binary category values.

        :return: dict of categories for tweets
        """
        """try:
            idlist=self.return_ids_list()
            cat_dict={}
            for id in idlist:
                cat_dict[id] = self.return_catmatrix_by_id(id)
        except Exception as e:
            raise
            #print('Error',e)
        return cat_dict"""
        try:
            cat_info = self.collection.find(projection = {'categories': 1})
            print(cat_info)
            cat_dict = dict()
            for item in cat_info:
                #print(item)
                cat_dict[item['_id']] = self.create_catmatrix(item.get('categories', []))
        except Exception as e:
            raise
            #print('Error',e)
        return cat_dict

    
    def return_text_all(self):
        """
        Lookup text for all tweets.

        :return: dictionary of id to text for all tweets
        """
        """try:
            idlist=self.return_ids_list()
            dic={}
            for id in idlist:
                dic[id] = self.find_text_by_id(id)
        except Exception as e:
            print('Error',e)
        return dic"""
        try:
            text_info = self.collection.find(projection = {'text': 1})
            #print(text_info)
            text_dict = dict()
            for item in text_info:
                #print(item)
                text_dict[item['_id']] = item.get('text')
        except Exception as e:
            raise
            #print('Error',e)
        return text_dict
    
    def return_priority_by_id(self,postid):
        """
        Return the priority of the given tweet

        :param postid: tweet to look up
        :return: priority of tweet
        """
        try:
             x = self.collection.find_one({"postID": str(postid)})
        except Exception as e:
            print("Error", e)
        return x["priority"]


    def return_classfier_dic(self):
        """
        Return a dictionary of id to [text, category] for all tweets in collection

        :return: dict of id to [text, category] 
        """
        try:
            idlist=self.return_ids_list()
            dic={}
            for id in idlist:
                dic.setdefault(id,[]).append([self.find_text_by_id(id),self.return_catmatrix_by_id(id)])
        except Exception as e:
            print('Error',e)
        return dic
