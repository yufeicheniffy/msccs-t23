# Class of the database functions
import pymongo
import json
import time
import sys


class DB:

    def __init__(self, client, db, name=" "):
        try:
            self.client =pymongo.MongoClient(client)
            print(self.client.test)
            #print(self.client.database_names())
            self.db = self.client[db]
            print(self.db)
        except pymongo.errors.ConnectionFailure:
            print("failed to connect")

    def insert(self, collection, item):
        self.collection = self.db[collection]
        try:
            self.collection.insert(item)
        except Exception as e:
            print("Error", e)

    def find_all(self, collection):
        self.collection = self.db[collection]
        try:
            x = self.collection.find()
        except Exception as e:
            print("Error", e)
        return x

    def find_category_by_id(self, collection, id):
        self.collection = self.db[collection]
        try:
            x = self.collection.find_one({"postID": str(id)})
        except Exception as e:
            print("Error", e)
        return x["categories"]

    def return_ids_list(self, collection):
        #self.collection = self.db[collection]
        l=[]
        all = self.find_all(collection)
        for e in all:
            l.append(e["postID"])
        return l

    def print_all(self, collection):
        for e in self.find_all(collection):
            print(e)
