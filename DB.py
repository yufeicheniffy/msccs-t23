# Class of the database functions
import pymongo
import json
import time
import sys


class DB:

    def __init__(self, client, db, name=" "):
        try:
            self.client =pymongo.MongoClient(client)
            print(self.client.database_names())
            self.db = self.client[db]
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

    def print_all(self, collection):
        for e in self.find_all(collection):
            print(e)
