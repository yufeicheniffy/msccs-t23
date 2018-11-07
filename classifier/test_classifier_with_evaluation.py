import sys
sys.path.insert(0, './data_files_scripts')

from Classify_with_evaluation import Classify
from data_files_scripts.MongoCollection import MongoCollection
# runs locally
training_connect = MongoCollection(collectionname='Training_token', MongoURI="mongodb://localhost:27017/")
test_connect = MongoCollection(collectionname='Test', MongoURI="mongodb://localhost:27017/")

#for computation reasons just test TWICE the first ytest works with all the TestCollection

# original train tes
"""training = training_connect.return_train_dic()
cat = list()
text = list()
#self.text_t = dict()
for tweet in sorted(training.keys()):
	cat.append(training[tweet][0][0])
	text.append(training_connect.find_text_by_id(tweet))
	#cat[tweet] = tweet_info[tweet][0][0]
	#text[tweet] = coll.find_text_by_id(tweet)
	#text_t[tweet] = tweet_info[tweet][0][1]

testing= test_connect.return_text_all()
cat_test = list()
text_test = list()
for tweet in sorted(testing.keys()):
	cat_test.append(testing[tweet][0][0])
	text_test.append(test_connect.find_text_by_id(tweet))"""

overall = training_connect.return_train_dic() + test_connect.return_text_all()
cat = list()
text = list()
for tweet in sorted(training.keys()):
	cat.append(training[tweet][0][0])
	text.append(training_connect.find_text_by_id(tweet))



clas = Classify(cat, text)
predict = clas.predict(text_test)
#returns a csv file with a dataframe
#clas.evaluation_(cat_test,predict)
clas.simple_evaluation(cat_test,predict)