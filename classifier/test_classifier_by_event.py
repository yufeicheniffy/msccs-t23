import sys
sys.path.insert(0, './data_files_scripts')
import sys
sys.path.insert(0, './classifier')

from Classify_with_evaluation import Classify
from data_files_scripts.MongoCollection import MongoCollection
from sklearn.model_selection import train_test_split
import numpy as np
import csv, argparse
from sklearn.svm import *
from sklearn.naive_bayes import BernoulliNB
from sklearn.ensemble import RandomForestClassifier

parser = argparse.ArgumentParser(description='Test classification.')
parser.add_argument('--out', action='store', default='eval.csv', required=False, dest='output_name')
parser.add_argument('--classifier', action='store', default='nb', required=False, dest='classifier')
parser.add_argument('--pretrained', action='store_true', dest='pretrained')
parser.add_argument('--save', action='store_true', dest='save')

args = parser.parse_args()
output_name = args.output_name
classifier = args.classifier
pretrained = args.pretrained
save = args.save

# runs locally
training_connect = MongoCollection(collectionname='Training_token', MongoURI="mongodb://localhost:27017/")
test_connect = MongoCollection(collectionname='Test', MongoURI="mongodb://localhost:27017/")

#resplit train/test
td0 = training_connect.return_text_all()
cd0 = training_connect.return_catdict_all()
ed0 = training_connect.return_event_all()
td1 = test_connect.return_text_all()
cd1 = test_connect.return_catdict_all()
ed1 = test_connect.return_event_all()

text_dict = {**td0, **td1}
cat_dict = {**cd0, **cd1}
event_dict = {**ed0, **ed1}
line_dict = dict()

full_text = list()
full_cat = list()
full_event = list()

for id in (sorted(text_dict.keys())):
	full_text.append(text_dict[id])
	full_cat.append(cat_dict[id])
	if event_dict[id][-2] == 'S':
		event_dict[id] = event_dict[id][:-2]
	full_event.append(event_dict[id])

# convert to array for indexing
full_event = np.array(full_event)
#print(set(event_dict.values()))

for event in set(event_dict.values()):
	print("\n\n\n")
	print("Event: ", event)

	test_rows = np.argwhere(full_event == event)
	train_rows = np.argwhere(full_event != event)
	
	text_test = [full_text[n[0]] for n in test_rows]
	cat_test = [full_cat[n[0]] for n in test_rows]
	
	text_train = [full_text[n[0]] for n in train_rows]
	cat_train = [full_cat[n[0]] for n in train_rows]

	cat_test_arr = np.array(cat_test, dtype=np.float64)
	if pretrained:
		clas = Classify(cat_train, pretrained='pretrained/')
	elif classifier == 'rf':
		clas = Classify(cat_train, text_train, 2000,
			model=RandomForestClassifier(class_weight='balanced', n_estimators=100))
	elif classifier == 'svc':
		clas = Classify(cat_train, text_train, 2000,
			model=SVC(class_weight='balanced'))
	elif classifier == 'linearsvc':
		clas = Classify(cat_train, text_train, 2000,
			model=LinearSVC(class_weight='balanced'))
	else: 
		clas = Classify(cat_train, text_train, 2000)
	predict = clas.predict(text_test)
	clas.simple_evaluation(cat_test,predict)

if save:
	clas.save_classifier()

