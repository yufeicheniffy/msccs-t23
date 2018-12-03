import app.search_rest as rest
import numpy as np
import sys
#sys.path.insert(0, '../')
#from classifier.Classify_with_evaluation import Classify
### This is a file used to test function, will be deleted later.. 
print("hello")
print(rest.query_search("PICS"))
catadictionary={'GoodsServices':0, 'SearchAndRescue':1,'InformationWanted':2,'Volunteer':3,'Donations':4,
                'MovePeople':5, 'FirstPartyObservation': 6, 'ThirdPartyObservation': 7, 'Weather': 8, 'EmergingThreats': 9,
                'SignificantEventChange':10, 'MultimediaShare': 11, 'ServiceAvailable': 12, 'Factoid': 13, 'Official': 14,
                'CleanUp':15, 'Hashtags': 16, 'PastNews': 17, 'ContinuingNews': 18, 'Advice': 19,
                'Sentiment':20, 'Discussion': 21, 'Irrelevant': 22, 'Unknown': 23, 'KnownAlready': 24,
                }
#comment
# a = np.random.randint(2,size=(25,))
# classifier = Classify(list(), pretrained='./classifier/pretrained/')
# mat_ = classifier.predict(["this is a text that got earthquake and help"])
# [0,1,0,1,0.,.,.,
# print(mat_)
# c = rest.categories_from_prediction(a)
# print(c)
