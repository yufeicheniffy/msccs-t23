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
       #the dictionary to find the catagory index in catarogy matrix.
    def __init__(self,collectionname='func_test',databasename='Helpme',MongoURI="mongodb://Admin_1:glasgowcom@cluster0-shard-00-00-0yvu9.gcp.mongodb.net:27017,cluster0-shard-00-01-0yvu9.gcp.mongodb.net:27017,cluster0-shard-00-02-0yvu9.gcp.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true"):
        """
        connect to cloud database default. chage to local,set:  MongoURI="mongodb://localhost:27017/"
        collections: Test;Train;Tweets; default:func_test to test
        create MongoClient instance
        """
        try:
            self.client = pymongo.MongoClient(MongoURI)
            print("connected to client:" + repr(self.client.list_database_names()))
            self.database = self.client[databasename]
            self.collection = self.database[collectionname]
        except pymongo.errors.ConnectionFailure:
            print("failed to connect")
            raise pymongo.errors.ConnectionFailure

    def insert(self, item):
        """
        Insert the given item to the collection

        :param item: item to insert
        """
        try:
            self.collection.insert(item)
        except Exception as e:
            print("Error", e)


    def find(self, query):
        """
        Find a document into this MongoCollection.

        :param query: query for search
        :return: documents returned by query
        """
        try:
            self.collection.find(query)
        except Exception as e:
            print("Error", e)

    def set_collection(self,collectionname): 
        """
        Change the collection to the given collection name.

        :param collectionname: collection to change to
        """
        if collectionname in ['Test',"Train","Training_token","TweetsData",'func_test']:
            self.collection=self.database[collectionname]
            return self
        else:
            raise collectionException
        

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
        try:
            return x["categories"]
        except TypeError:
            print('No Tweets found, check the postID')
            raise TypeError

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

    def find_text_by_ids(self,postidlist):
        """
        Lookup the text of the given tweet.

        :param postid: tweet id list to lookup
        :return: List of tweet
        """
        try:
            textlist=[]
            for id in postidlist:
                x = self.collection.find_one({"identifier": str(id)})
                if (x is None):
                    x = self.collection.find_one({"postID": str(id)})
                textlist.append(x["text"])
        except Exception as e:
            print("Error\n", e)
            print('can not find the text, please check the postidlist')
            raise e
        return textlist

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
        Return binary array for with 0/1 for the existance of each category
        label for the given tweet. This is done in order of the values
        in the catadictionary.

        :param postid: tweet to search
        :return: array of 0s and 1s
        """
        try:
            catmatrix=np.full((25,), 0)
            catalist=self.find_category_by_id(postid)
            for e in catalist:
                i=self.catadictionary.get(e)
                catmatrix[i]=1
        except Exception as e:
            print("Error", e)
            raise e
        return catmatrix

    def return_catmatrix_all(self):
        """
        Return the categories vector according to catagory dictionary.

        :return: array of category arrays for all posts
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
        Return a binary category array for a tweet with the given categories.

        :param categories: list of categories
        :return: array of binary values
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
        try:
            cat_info = self.collection.find(projection = {'categories': 1})
            #print(cat_info)
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

    def return_event_by_id(self,postid):
        """
        Return the event of the given tweet

        :param postid: tweet to look up
        :return: event of tweet
        """
        try:
             x = self.collection.find_one({"postID": str(postid)})
        except Exception as e:
            print("Error", e)
        return x["event"]

    def return_event_all(self):
        """
        Lookup event for all tweets.

        :return: dictionary of id to event for all tweets
        """
        try:
            event_info = self.collection.find(projection = {'event': 1})
            #print(text_info)
            event_dict = dict()
            for item in event_info:
                #print(item)
                event_dict[item['_id']] = item.get('event')
        except Exception as e:
            raise
            #print('Error',e)
        return event_dict


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


    def return_tweets_by_category(self, category):
        """
        Return tweets belonging to the given category.

        :param category: category to search for
        :return: list of tweet ids in the given category
        """
        try:
            x = self.collection.find({"categories": str(category)})
        except Exception as e:
            print("Error", e)
        list_return = []
        for t in x:
            list_return.append(t["postID"])
        return list_return

    def return_tweets_by_event(self, event):
        """
        Return tweets belonging to the given event.

        :param event: event to search for
        :return: list of tweet ids in the given event
        """
        try:
            x = self.collection.find({"event": str(event)})
        except Exception as e:
            print("Error", e)
        list_return = []
        for t in x:
            list_return.append(t["postID"])
        return list_return

    def return_tweets_by_priority(self,priority):
        """
        Return tweets belonging to the given priority.

        :param category: priority to search for
        :return: list of tweet ids in the given priority
        """
        try:
            x = self.collection.find({"priority": str(priority)})
        except Exception as e:
            print("Error", e)
        list_return = []
        for t in x:
            list_return.append(t["postID"])
        return list_return
    
    def updata_category_by_id(self,postid,category):
        """
        updata category for given Tweets

        :param category: postid, category
        :return: -
        """
        try:
            myquery = { "postID": postid }
            newvalues = { "$set": { "categories": category } }
            self.collection.update_many(myquery,newvalues)
        except Exception as e:
            print("Error", e)

    def updata_event_by_ids(self,postidlist,eventname):
        """
        updata event for a list of given Tweets

        :param category: a list of postid and correspongding list of eventname
        :return: -
        """
        try:
            for i in range(0,len(postidlist)):
                myquery = { "postID": postidlist[i] }
                newvalues = { "$set": { "event": eventname[i] } }
                self.collection.update_many(myquery,newvalues)
        except Exception as e:
            print("Error", e)
    
class collectionException(Exception):
    print('your collection is not in our collection list, please read Readme.md to set correct collections')
    pass