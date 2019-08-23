import sys
import time
import tweepy
from dateutil import parser
import calendar
import numpy as np
import unittest

# Unit Testing For Tweets processing

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

def connect_to_api(access_token, access_token_secret):
    try:
        auth = tweepy.AppAuthHandler(access_token, access_token_secret)
        return 1
    except Exception as e:
        print(e)
        return -1


def sort_results(dictionaries):
    return sorted(dictionaries, key=lambda k: k['Retweets'], reverse=True)
class MyTest(unittest.TestCase):
    def test(self):
        self.assertEqual(connect_to_api("CdyttfRtpEkoJqvDnhsJOY7pj","dtIeA7h9P6gQdfL6jsh2xI9dOLunBQfji5xI6Up6nrN1t9M6Zu"),1)
    'Categories from Prediction'
    def test2(self):
        p_m = np.matrix([1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
        p_m.reshape(1,25)
        print(categories_from_prediction(p_m))
        result_list= ["GoodsServices","InformationWanted"]
        self.assertEqual(categories_from_prediction(p_m),result_list)

    '''Priority from Category'''
    def test3(self):
        #High
        cat_1 = ["GoodsServices","InformationWanted"]
        #High
        cat_2 = ['GoodsServices','Official','Discussion']
        # medium
        cat_3 = ['Official','Donations']
        #medium
        cat_4 = ['Official','Discussion']
        #low
        cat_5 = ['Sentiment', 'Discussion']
        self.assertEqual(category_to_priority(cat_1), 'High')
        self.assertEqual(category_to_priority(cat_2), 'High')
        self.assertEqual(category_to_priority(cat_3), 'Medium')
        self.assertEqual(category_to_priority(cat_4), 'Medium')
        self.assertEqual(category_to_priority(cat_5), 'Low')

    def test4(self):
        dicts = [{'id': 2, 'Retweets':20},{'id': 21, 'Retweets':210},{'id': 22, 'Retweets':190}]
        correct_result= [{'id': 21, 'Retweets':210}, {'id': 22, 'Retweets':190}, {'id': 2, 'Retweets':20}]
        wrong_result = [{'id': 22, 'Retweets':190}, {'id': 21, 'Retweets':210}, {'id': 2, 'Retweets':20}]
        self.assertEqual(sort_results(dicts), correct_result)
        self.assertEqual(sort_results(dicts), wrong_result)
        #by retweets








if __name__ == '__main__':
    unittest.main()
