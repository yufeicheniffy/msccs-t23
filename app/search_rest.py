import datetime
import time
import tweepy
import pymongo
import sys
import json
from bson import json_util, ObjectId
from dateutil import parser
import calendar


#git example


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
    for tweet in tweepy.Cursor(api.search, q=query, lang="en", count=5).items():
        if(time.time()> time_started+2):
			#mycol_all.insert(result_list)
            print(type(datetime_created))
            return result_list, id_list
        # result_list.append(json.loads(json_util.dumps({"Postid": tweet["idstr"], "Text": tweet["text"]})))
        if ("media" in tweet._json["entities"]):
            tweet_media = True
        else:
            tweet_media = False
        datetime_created = parser.parse(tweet._json["created_at"])
        result_list.append({"Postid": tweet._json["id_str"], "Text": tweet._json["text"], "Media": tweet_media, "Datetime": datetime_created, "DateString": tweet._json["created_at"], "timestamp": calendar.timegm(parser.parse(tweet._json["created_at"]).timetuple())})
        id_list.append(tweet._json["id_str"])
