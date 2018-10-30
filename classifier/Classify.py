from MongoCollection import MongoCollection
from sklearn.naive_bayes import BernoulliNB
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
import numpy as np

class Classify:
	def __init__(self, collectionname='Training_token', databasename='Helpme', \
		MongoURI="mongodb://Admin_1:glasgowcom@cluster0-shard-00-00-0yvu9.gcp.mongodb.net:27017,cluster0-shard-00-01-0yvu9.gcp.mongodb.net:27017,cluster0-shard-00-02-0yvu9.gcp.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true"):
		self.coll=MongoCollection(collectionname=collectionname, databasename=databasename, \
			MongoURI=MongoURI)
		#coll.find_text_by_id('243374590288592896')
		self.tweet_info = self.coll.return_train_dic()
		self.cat = list()
		self.text = list()
		#self.text_t = dict()

		for tweet in sorted(self.tweet_info.keys()):
		    #cat[tweet] = tweet_info[tweet][0][0]
		    #text[tweet] = coll.find_text_by_id(tweet)
		    #text_t[tweet] = tweet_info[tweet][0][1]
		    self.cat.append(self.tweet_info[tweet][0][0])
		    self.text.append(self.coll.find_text_by_id(tweet))

		self.vectorizer = CountVectorizer(stop_words=stopwords.words(),binary=True)
		self.vect_train = self.vectorizer.fit_transform(self.text)

		print(self.vectorizer.get_feature_names())

		self.cat_arr = np.array(cat)

		print(len(cat_arr[:,0]))

		self.classifiers = list()


	def train():
		"""
		Fits classifiers to the training data we already have.
		"""
		#len(categories)
		for i in range(0, len(cat_arr[0])):
		    c = BernoulliNB().fit(vect_train, cat_arr[:,i])
		    self.classifiers.append(c)

		 print("Training complete!")


	def predict(tweets):
		"""
		Returns an array of predictions for the given features.

		:param tweets: a list of string tweets
		:throws: 
		"""
		if len(self.classifiers) == 0:
			raise RuntimeError("Classifiers have not been trained!")

		tokenized = self.vectorizer.transform(tweets)
		predictions = np.zeros(len(tweets), len(self.classifiers))

		for i in len(classifiers):
			predictions[:,i] = self.classifiers[i].predict(tokenized)

		print(predictions)
		return(predictions)











