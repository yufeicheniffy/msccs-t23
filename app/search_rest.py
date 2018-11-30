import sys
import time
import tweepy
import pymongo
from dateutil import parser
import calendar
import numpy as np
#sys.path.insert(0, '../')
#from classifier.Classify_with_evaluation import Classify


#classifier_ = Classify(list(), pretrained='../classifier/pretrained')
#classifier_.predict([lala])
#git example
catadictionary={'GoodsServices':0, 'SearchAndRescue':1,'InformationWanted':2,'Volunteer':3,'Donations':4,
                'MovePeople':5, 'FirstPartyObservation': 6, 'ThirdPartyObservation': 7, 'Weather': 8, 'EmergingThreats': 9,
                'SignificantEventChange':10, 'MultimediaShare': 11, 'ServiceAvailable': 12, 'Factoid': 13, 'Official': 14,
                'CleanUp':15, 'Hashtags': 16, 'PastNews': 17, 'ContinuingNews': 18, 'Advice': 19,
                'Sentiment':20, 'Discussion': 21, 'Irrelevant': 22, 'Unknown': 23, 'KnownAlready': 24,
                }


def category_to_priority(categories):
    catadictionary_prio={'GoodsServices':'High', 'SearchAndRescue':"High",'InformationWanted':"High",'Volunteer':"Low",'Donations':"Medium",
                    'MovePeople':"High", 'FirstPartyObservation': "Low", 'ThirdPartyObservation': 'Low', 'Weather': "Low", 'EmergingThreats': "High",
                    'SignificantEventChange':"High", 'MultimediaShare': "Low", 'ServiceAvailable': "High", 'Factoid': "Low", 'Official': "Medium",
                    'CleanUp':"Low", 'Hashtags': "Low", 'PastNews': "Low", 'ContinuingNews': "Low", 'Advice': "Low",
                    'Sentiment':"Low", 'Discussion': "Low", 'Irrelevant': "Low", 'Unknown': "Low", 'KnownAlready': "Low"}
    list_categories = []
    for c in categories:
        list_categories.append(catadictionary_prio[c])
    priority =""
    if("High" in list_categories):
        priority = "High"
    elif("Medium" in list_categories):
        priority="Medium"
    elif ("Low" in list_categories):
        priority ="Low"
    return priority




def categories_from_prediction(prediction_matrix):
    categories_list = []
    list_cata = list(catadictionary)
    for i in range(prediction_matrix.shape[0]):
        if(prediction_matrix[i]==1):
            categories_list.append(list_cata[i])
    return categories_list


def query_search(query):
    api_key = "CdyttfRtpEkoJqvDnhsJOY7pj"
    api_key_secret = "dtIeA7h9P6gQdfL6jsh2xI9dOLunBQfji5xI6Up6nrN1t9M6Zu"
    auth = tweepy.AppAuthHandler(api_key, api_key_secret)
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
        if(time.time()> time_started+5):
            sort_result = sorted(result_list, key=lambda k: k['Retweets'], reverse=True)
            return sort_result, id_list
        # result_list.append(json.loads(json_util.dumps({"Postid": tweet["idstr"], "Text": tweet["text"]})))
        if ("media" in tweet._json["entities"]):
            tweet_media = True
        else:
            tweet_media = False
        # prediction
        #categories_ = categories_from_prediction(classifier_.predict([t["Text"]]))
        prediction_matrix= np.random.randint(2,size=(25,))
        categories_ =categories_from_prediction(prediction_matrix)
        priority_ = category_to_priority(categories_)
        retweets_counter = tweet._json["retweet_count"]
        datetime_created = parser.parse(tweet._json["created_at"])
        result_list.append({"Postid": tweet._json["id_str"], "Text": tweet._json["text"], "Media": tweet_media, "Datetime": datetime_created, "DateString": tweet._json["created_at"], "timestamp": calendar.timegm(parser.parse(tweet._json["created_at"]).timetuple()), "Retweets": retweets_counter,"Category": categories_, "Priority": priority_})
        id_list.append(tweet._json["id_str"])
