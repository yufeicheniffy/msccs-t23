from DB import DB
from Reader import Reader
from twitter_api import twitter_api
from MongoCollection import MongoCollection
import json

collection = MongoCollection()
#database = DB("mongodb://Admin_1:glasgowcom@cluster0-shard-00-00-0yvu9.gcp.mongodb.net:27017,cluster0-shard-00-01-0yvu9.gcp.mongodb.net:27017,cluster0-shard-00-02-0yvu9.gcp.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true", "mscdb", "msc")
read = Reader("name of the reader")
l = read.read("TRECIS-CTIT-H-Training.json")
twitter = twitter_api("access_token", "access_token_secret", collection)
#first parameter is the collection.
collection.insert()
collection.print_all()
ids = collection.return_ids_list()
text_from_ids = twitter.list_from_ids(ids)
collection.insert("text_tweets", twitter.transform_to_dict(text_from_ids))
tweet_dict= twitter.find_from_id(1050488732187385856)
twitter.search_query("earthquake")
