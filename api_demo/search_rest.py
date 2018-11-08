import datetime
import time
import tweepy
import pymongo
import sys
import json
from bson import json_util, ObjectId


def query_search(query):
    access_token = "IHpSjYd5AuCdDRZTaGiMOwHUJ"
    access_token_secret = "FNUvxez9N9vBzY72HiZcukHQqVqO0ZiV498qyaYDxaV5nKFSgu"
    auth = tweepy.AppAuthHandler(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    if (not api):
        print("Can't Authenticate")
        sys.exit(-1)

    time_started = time.time()
    result_list = []
    id_list = []
    # You can change the cound the time limit of search.
    # moreover we can use Stream to be realy real_life project
    for tweet in tweepy.Cursor(api.search, q=query, lang="en", count=10).items():
        if(time.time()> time_started+2):
			#mycol_all.insert(result_list)
            return result_list, id_list
        # result_list.append(json.loads(json_util.dumps({"Postid": tweet["idstr"], "Text": tweet["text"]})))

        result_list.append({"Postid": tweet._json["id_str"], "Text": tweet._json["text"]})
        id_list.append(tweet._json["id_str"])
