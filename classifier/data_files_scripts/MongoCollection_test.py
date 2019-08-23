import unittest
from MongoCollection import MongoCollection
from MongoCollection import collectionException
import pymongo 

# Before run this test, make sure you can connect to database. Both local database and cloud database.
class MongoCollection_test(unittest.TestCase):
    def test_find_text_by_ids(self):
        collection=MongoCollection(MongoURI='mongodb://localhost:27017/')
        collection.set_collection('TweetsData')
        self.assertEqual(collection.find_text_by_ids(postidlist=["266269932671606786","266804609954234369","266250638852243457"]),["Eight dead in the 7.5 magnitude earthquake in Guatemala","RT @adamlevine: Guys, let's help raise funds for the @RedCross for those in need in the #Guatemala #earthquake http://t.co/6u9oY7sh","RT @wxdude: My heart goes out to people in #Guatemala: A deadly 7.4 #earthquake hit earlier 101 miles WSW of Guatemala City; at least 10 ..."])
    
    def test_return_catamatrix_by_id(self):
        collection=MongoCollection(MongoURI='mongodb://localhost:27017/')
        collection.set_collection('TweetsData')
        print(collection.return_catmatrix_by_id(postid="267830654174126080"))
    
    def test_find_text_by_ids2(self):
        with self.assertRaises(Exception):
            collection=MongoCollection(MongoURI='mongodb://localhost:27017/')
            collection.set_collection('TweetsData')
            collection.return_catmatrix_by_id(postid="123456789")

    def test_init1(self):
        collection=MongoCollection()
        self.assertEqual(collection.client,pymongo.MongoClient("mongodb://Admin_1:glasgowcom@cluster0-shard-00-00-0yvu9.gcp.mongodb.net:27017,cluster0-shard-00-01-0yvu9.gcp.mongodb.net:27017,cluster0-shard-00-02-0yvu9.gcp.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true"))
        self.assertEqual(collection.database,collection.client['Helpme'])
        self.assertEqual(collection.collection,collection.database['func_test'])

    def test_init2(self):
        collection=MongoCollection(collectionname='TweetsData',databasename='Helpme',MongoURI='mongodb://localhost:27017/')
        self.assertEqual(collection.client,pymongo.MongoClient('mongodb://localhost:27017/'))
        self.assertEqual(collection.database,collection.client['Helpme'])
        self.assertEqual(collection.collection,collection.database['TweetsData'])

    def test_init3(self):
        with self.assertRaises(pymongo.errors.ConnectionFailure):
            MongoCollection(collectionname='Tweets',databasename='Helpme',MongoURI='mongodb://localhost:27015/')
            
    def test_setcollection1(self):
        collection=MongoCollection(MongoURI='mongodb://localhost:27017/')
        collection.set_collection('Test')
        self.assertEqual(collection.collection,collection.database['Test'])

    def test_setcollection2(self):
        with self.assertRaises(collectionException):
            collection=MongoCollection(MongoURI='mongodb://localhost:27017/')
            collection.set_collection('Wrongcollection')

    def test_find_category_by_id(self):
        collection=MongoCollection(MongoURI='mongodb://localhost:27017/')
        collection.set_collection('TweetsData')
        self.assertEqual(collection.find_category_by_id(postid="266269932671606786"),["EmergingThreats","Factoid","KnownAlready"])
    
    def test_find_category_by_id2(self):
        with self.assertRaises(TypeError):
            collection=MongoCollection(MongoURI='mongodb://localhost:27017/')
            collection.set_collection('TweetsData')
            collection.find_category_by_id("123456789")

    def test_find_text_by_ids2(self):
        with self.assertRaises(Exception):
            collection=MongoCollection(MongoURI='mongodb://localhost:27017/')
            collection.set_collection('TweetsData')
            find_text_by_ids(postidlist=["123456789","987654321"])

    def test_return_ids_list(self): # Tested in 'Training_token' collection.
        collection=MongoCollection(MongoURI='mongodb://localhost:27017/')
        collection.set_collection('Training_token')
        self.assertEqual(len(collection.return_ids_list()),1235)
    


    
    
    



