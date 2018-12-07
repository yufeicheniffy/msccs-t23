import sys
import time
import tweepy
from dateutil import parser
import calendar
import numpy as np
sys.path.insert(0, '../')
from classifier.Classify_with_evaluation import Classify


classifier_ = Classify(list(), pretrained='./classifier/pretrained/')
'''
a dictionary which provides ids at each ontology
'''
catadictionary={'GoodsServices':0, 'SearchAndRescue':1,'InformationWanted':2,'Volunteer':3,'Donations':4,
                'MovePeople':5, 'FirstPartyObservation': 6, 'ThirdPartyObservation': 7, 'Weather': 8, 'EmergingThreats': 9,
                'SignificantEventChange':10, 'MultimediaShare': 11, 'ServiceAvailable': 12, 'Factoid': 13, 'Official': 14,
                'CleanUp':15, 'Hashtags': 16, 'PastNews': 17, 'ContinuingNews': 18, 'Advice': 19,
                'Sentiment':20, 'Discussion': 21, 'Irrelevant': 22, 'Unknown': 23, 'KnownAlready': 24,
                }

'''
input : a list of categories
return : the priority of the tweet
method: transform the categories list into a priority list with the help of category priority matrix-
        and returns the most important category of the list.
'''
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



'''
input : a binary np.matrix(25,1)
return: a list of categories
method: the input matrix contains 1 at a cell, if the classifier returned true for the category that this cell is representing.

'''
def categories_from_prediction(prediction_matrix):
    categories_list = []
    list_cata = list(catadictionary)
    for i in range(prediction_matrix.shape[1]):
        if(prediction_matrix[0,i]==1):
            categories_list.append(list_cata[i])
    return categories_list

'''
input: keyword, number of tweets to be retrieved
return a list of ids, a list of dictionaries with tweet attributes, a sorted list of tweets based on retweet_count
method: fully explained at the report. section: 4.3.1.1
'''
def query_search(query, tweet_num):
    time_to_search=time.time()
    print('starting time: ',time_to_search)
    api_key = "CdyttfRtpEkoJqvDnhsJOY7pj"
    api_key_secret = "dtIeA7h9P6gQdfL6jsh2xI9dOLunBQfji5xI6Up6nrN1t9M6Zu"
    try:
        auth = tweepy.AppAuthHandler(api_key, api_key_secret)
        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        if (not api):
            print("Can't Authenticate")
            sys.exit(-1)
    except Exception as e:
        print("auth error",e)

    time_started = time.time()
    result_list = []
    id_list = []
    matrix_allcate=np.zeros((1,25))
    dic_catagories={'Request':[],'Calls':[],'Report':[],'Others':[]}
    counter=0.0
    for tweet in tweepy.Cursor(api.search, q=query, lang="en", count=60).items():
        if(time.time()> time_started+60 or len(id_list)==int(tweet_num)):
            print('\n now have \n',len(id_list))
            sort_result = sorted(result_list, key=lambda k: k['Retweets'], reverse=True)
            matrix_allcate=np.where(matrix_allcate>0,1,0)
            for cat in categories_from_prediction(matrix_allcate):
                if cat in ['GoodsServices', 'SearchAndRescue','InformationWanted']:
                    dic_catagories['Request'].append(cat)
                if cat in ['Volunteer','Donations','MovePeople']:
                    dic_catagories['Calls'].append(cat)
                if cat in ['FirstPartyObservation', 'ThirdPartyObservation', 'Weather', 'EmergingThreats','SignificantEventChange', 'MultimediaShare', 'ServiceAvailable', 'Factoid', 'Official','CleanUp', 'Hashtags']:
                    dic_catagories['Report'].append(cat)
                if cat in ['PastNews', 'ContinuingNews', 'Advice','Sentiment', 'Discussion', 'Irrelevant', 'Unknown', 'KnownAlready']:
                    dic_catagories['Others'].append(cat)

            print('This search contain following catagories:/n',dic_catagories)
            print("finished after ", time.time()-time_to_search)
            return sort_result, id_list, dic_catagories
        # result_list.append(json.loads(json_util.dumps({"Postid": tweet["idstr"], "Text": tweet["text"]})))
        if  ('RT @' not in tweet._json['text']):
            counter+=1
            if ("media" in tweet._json["entities"]):
                tweet_media = True
            else:
                tweet_media = False

            prediction_matrix= (classifier_.predict([tweet._json["text"]]))
            matrix_allcate+=prediction_matrix
            if np.sum(prediction_matrix)==0:
                categories_=['Unknown']
            else:
                categories_ =categories_from_prediction(prediction_matrix)
            priority_ = category_to_priority(categories_)
            timestamp = calendar.timegm(parser.parse(tweet._json["created_at"]).timetuple())
            if "retweeted_status" in tweet._json:
                timestamp = calendar.timegm(parser.parse(tweet._json["retweeted_status"]["created_at"]).timetuple())
            retweets_counter = tweet._json["retweet_count"]
            datetime_created = parser.parse(tweet._json["created_at"])
            result_list.append({"Postid": tweet._json["id_str"], "Text": tweet._json["text"], "Media": tweet_media, "Datetime": datetime_created, "DateString": tweet._json["created_at"], "timestamp": timestamp, "Retweets": retweets_counter,"Category": categories_, "Priority": priority_})
            id_list.append(tweet._json["id_str"])
