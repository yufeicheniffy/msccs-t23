import sys
sys.path.insert(0, './data_files_scripts')

from MongoCollection import MongoCollection
from sklearn.naive_bayes import BernoulliNB
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
import numpy as np
import pymongo
from sklearn.metrics import f1_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import accuracy_score
import pandas as pd


class Classify:
	"""
	A classifier which pulls tweet data from the mongodb database.
	"""

	def __init__(self, collectionname='Training_token', databasename='MasterProject',
		MongoURI="mongodb://localhost:27017/"):
		"""
		Create classifier. Does not train classifier -- Use .train to do that.
		"""
		self.categories=[
		    "Advice",
		    "CleanUp",
		    "ContinuingNews",
		    "Discussion",
		    "Donations",
		    "EmergingThreats",
		    "Factoid",
		    "FirstPartyObservation",
		    "GoodsServices",
		    "Hashtags",
		    "InformationWanted",
		    "Irrelevant",
		    "KnownAlready",
		    "MovePeople",
		    "MultimediaShare",
		    "Official",
		    "PastNews",
		    "SearchAndRescue",
		    "Sentiment",
		    "ServiceAvailable",
		    "SignificantEventChange",
		    "ThirdPartyObservation",
		    "Unknown",
		    "Volunteer",
		    "Weather"
		]
		self.coll=MongoCollection(collectionname=collectionname, databasename=databasename, \
			MongoURI=MongoURI)
		#coll.find_text_by_id('243374590288592896')
		self.tweet_info = self.coll.return_train_dic()
		self.cat = list()
		self.text = list()
		#self.text_t = dict()
		for tweet in sorted(self.tweet_info.keys()):
			self.cat.append(self.tweet_info[tweet][0][0])
			self.text.append(self.coll.find_text_by_id(tweet))



		    #cat[tweet] = tweet_info[tweet][0][0]
		    #text[tweet] = coll.find_text_by_id(tweet)
		    #text_t[tweet] = tweet_info[tweet][0][1]
		self.cat_arr = np.array(self.cat)
		print(self.cat)
		print(self.cat_arr)

		self.vectorizer = CountVectorizer(stop_words=stopwords.words(),binary=True)
		self.vect_train = self.vectorizer.fit_transform(self.text)

		print(self.vectorizer.get_feature_names())

		# myclient_ = pymongo.MongoClient("mongodb://localhost:27017/")
		# mydb = myclient_["MasterProject"]
		# mycol = mydb["Terms"]
		# mycol.insert({"TermDoc":"Terms", "Array": self.cat_arr})

		print(len(self.cat_arr[:,0]))

		self.classifiers = list()


	def train(self):
		"""
		Fits classifiers to the training data we already have.
		"""
		#len(categories)
		for i in range(0, len(self.cat_arr[0])):
		    c = BernoulliNB().fit(self.vect_train, self.cat_arr[:,i])
		    self.classifiers.append(c)

		print("Training complete!")

	#retrieves the index of category eg 0 = 'Advice'
	def map_id(self,category):
	    returner = []
	    for c in category:
	        for i in range(0,len(self.categories)):
	            if(c == self.categories[i]):
	                returner.append(i)
	    return returner


#	it would be lists of lists [true_labels0 = [label1,label2,], true_labels1 = [label1]]
#	create the binary Test x Categoriy matrix : each row of matrix represent the true categories of each Test data->
#	[Binary_category1,....,Binary_categorym,.......Binary_category25]
	def create_binary_category(self,ytest_array):
		returner = np.zeros(25)[:None]

		for ytest in ytest_array:
			#checking if is a simple text, without this if the for would iterate to every char of string
			if isinstance(ytest, str):
			    ytest= [ytest]
			id_1 = self.map_id(ytest)
			category_arr = np.zeros(25)[:None]
			for id in id_1:
				category_arr[id]=1
			returner = np.vstack((returner, category_arr))	

		return returner[1:,:]

#	input ytest_array,and X_test
	def evaluation_(self,ytest_array,predict):
		listdic = []
		data_v = []
		y_test_arr = self.create_binary_category(ytest_array)
		print("y_test_array")
		print(y_test_arr)
		print("Predictions")
		print(predict)
		for i in range(0,len(self.categories)):
		    listdic.append({"Category": self.categories[i], "Accuracy": accuracy_score(y_test_arr[:,i],predict[:,i]), "Recall": recall_score(y_test_arr[:,i],predict[:,i],pos_label=1), "Preccision": precision_score(y_test_arr[:,i],predict[:,i],pos_label=1), "F1score":f1_score(y_test_arr[:,i],predict[:,i],pos_label=1)})
		    data_v.append(accuracy_score(y_test_arr[:,i],predict[:,i]))
		    data_v.append(recall_score(y_test_arr[:,i],predict[:,i],pos_label=1))
		    data_v.append(precision_score(y_test_arr[:,i],predict[:,i],pos_label=1))
		    data_v.append(f1_score(y_test_arr[:,i], predict[:,i], pos_label=1))

		data_v = np.array(data_v)
		data_v = data_v.reshape(25,4)
		data_frame = pd.DataFrame(data=data_v, index=np.array(self.categories),columns=np.array(['Accuracy', 'Precision', 'Recall', 'F1 Score']))
		print(data_frame)
		data_frame.to_csv('evaluation.csv', sep='\t')
		return data_frame


	def predict(self,tweets):
		"""
		Returns an array of predictions for the given features.

		:param tweets: a list or array of string tweets
		:returns: predictions matrix

		:throws RuntimeError: if classifiers have not been trained
		"""
		if len(self.classifiers) == 0:
			raise RuntimeError("Classifiers have not been trained!")

		tokenized = self.vectorizer.transform(tweets)
		predictions = np.zeros((len(tweets), len(self.classifiers)))

		for i in range(0, len(self.classifiers)):
			predictions[:,i] = self.classifiers[i].predict(tokenized)

		#print(predictions)
		return(predictions)
