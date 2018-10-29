import tweepy
import sys
import json
import time


class twitter_api:
    def __init__(self, access_token, access_token_secret, DB):
        self.DB = DB
        auth = tweepy.AppAuthHandler(access_token, access_token_secret)
        self.api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        if(not self.api):
            print("Cannot Authenticate")
            sys.exit(-1)
# input a list with ids
# returns a list with dictionary elements
#tweepy has a look up method. However it can only retrive 100 tweets per call
#results : statuses_lookup doesnt retrive every 100 tweets have been deleted
# we lose 98 tweet texts

    def list_from_ids(self, ids):
        list = []
        ids_len = len(ids)
        #integer divide
        iterations = ids_len//100
        # eg 202 ids last_ids = 202- 2*100 = 2
        last_ids = ids_len - iterations*100
        #we iterate till last_ids
        start = 0
        end = 99
        # we start from 1 in order to slice the list
        for i in range(1, iterations+1):
            tweets = (self.api.statuses_lookup(ids[start:end]))
            for t in tweets:
                c = self.DB.find_category_by_id("test", t.id)
                list.append({"postID": t.id, "text": t.text, "category": c})
            #for first iteration new start = 100 and end (1+1)*100-1 = 199
            #we dont care that at the next iteration will overide the len of list
            # because for loop is terminated.
            start = end+1
            end = (i+1)*100-1
        #iterate through the last ids
        #for our example we start from 200
        # and we end at 200+2-1 = 201 because arrays starts from 0
        start = iterations*100
        tweets = self.api.statuses_lookup(ids[start:start+last_ids-1])
        print(start+last_ids-1)
        for t in tweets:
            c = self.DB.find_category_by_id("test", t.id)
            list.append({"postID": t.id, "text": t.text, "category": c})
        
        return list
#find one tweet maybe will be used for testing

    def find_from_id(self, id):
        tweet = self.api.get_status(id)
        tweet_json = tweet._json

        return self.make_dictionary(tweet_json)

    def search_query(self, event):
        for tweets in tweepy.Cursor(self.api.search, q=event, lang="en", result_type="recent", count=100).items():
            print(self.make_dictionary(tweets._json))


#dictionary{id,text,user,coords,media}
#will help to visualise live events.
    def make_dictionary(self, tweet_json):
        tweet_text = tweet_json["text"]
        tweet_user = tweet_json["user"]["screen_name"]
        #long,lat
        if(tweet_json["coordinates"] is not None):
            tweet_cordinates = tweet_json["coordinates"]["coordinates"]
        else:
            tweet_cordinates = []
        tweet_entities = tweet_json["entities"]
        if(tweet_entities["urls"] is not None):
            tweet_urls = tweet_entities["urls"]
        else:
            tweet_urls = []
        if("media" in tweet_entities):
            tweet_media = tweet_entities["media"]
        else:
            tweet_media = []
        tweet_dict = {"id": id, "text": tweet_text, "user": tweet_user, "coords": tweet_cordinates, "urls": tweet_urls, "media": tweet_media}
        return tweet_dict

    #transforms to simple dict of {text}
    def transform_to_textdict(self, list):

        returner = [{"text": x} for x in list]

        return returner
