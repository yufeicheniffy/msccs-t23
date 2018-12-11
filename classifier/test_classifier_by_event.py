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
from sklearn.linear_model import LogisticRegression

parser = argparse.ArgumentParser(description='Test classification.')
parser.add_argument('--out', action='store', default='results/eval.csv', required=False, dest='output_name')
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

full_event = np.array(full_event)

# leave one event out for testing each time
full_res = {'Number of Predictions': 0, 'True Positive': 0,
			'True Negative': 0, 'False Positive': 0,
			'False Negative': 0, 'One Label': 0,
			'Perfect Match': 0}

max_res = {'Number of Predictions': 0, 'True Positive': 0,
			'True Negative': 0, 'False Positive': 0,
			'False Negative': 0, 'One Label': 0,
			'Perfect Match': 0}

full_cat_confusion = dict()
for event in set(event_dict.values()):
	#print("\n\n")
	print("Event: ", event)

	test_rows = np.argwhere(full_event == event)
	train_rows = np.argwhere(full_event != event)
	
	text_test = [full_text[n[0]] for n in test_rows]
	cat_test = [full_cat[n[0]] for n in test_rows]
	
	text_train = [full_text[n[0]] for n in train_rows]
	cat_train = [full_cat[n[0]] for n in train_rows]

	cat_test_arr = np.array(cat_test, dtype=np.float64)
	if pretrained:
		clas = Classify(pretrained='pretrained/')
	elif classifier == 'rf':
		clas = Classify(text_train, cat_train, 2000,
			model=RandomForestClassifier(class_weight='balanced', 
				n_estimators=1))
	elif classifier == 'lsvc':
		clas = Classify(text_train, cat_train, 2000,
			model= LinearSVC(C = 0.01,
				class_weight = 'balanced',
				loss = 'hinge',
				random_state=1))
	elif classifier == 'log':
		clas = Classify(text_train, cat_train, 2000,
			model=LogisticRegression(class_weight='balanced',
				loss = 'hinge', C = 0.01))
	else:
		clas = Classify(text_train, cat_train, 2000)
	predict = clas.predict(text_test)
	simp = clas.evaluate(cat_test, predict)
	cat_confusion = clas.mat_all_categories(cat_test, predict)
	
	#for key in simp:
	#	print(key, ": ", simp[key])

	for key in simp:
		if key in full_res:
			full_res[key] += simp[key]
		if key in max_res:
			max_res[key] = max(max_res[key], simp[key])
		else:
			max_res[key] = simp[key]

	if len(full_cat_confusion) == 0:
		full_cat_confusion = cat_confusion
	else:
		for cat in cat_confusion:
			for key in cat_confusion[cat]:
				full_cat_confusion[cat][key] += cat_confusion[cat][key]

stats = clas.stats_calc(full_res['True Positive'], 
            full_res['True Negative'], full_res['False Positive'], 
            full_res['False Negative'], full_res['One Label'], 
            full_res['Perfect Match'])

full_res = {**full_res, **stats}
print("\n\nOverall Results: ")
for key in full_res:
		print(key, ": ", full_res[key])

"""print("\n\nBest Results: ")
for key in ['One Label Score', 'Perfect Match Score', 
	'Accuracy', 'Precision', 'Recall', 'F1 Score']:
		print(key, ": ", max_res[key])"""



cat_stats = list()
for key in full_cat_confusion:
	s = clas.stats_calc(
			full_cat_confusion[key]['True Positive'], 
            full_cat_confusion[key]['True Negative'], 
            full_cat_confusion[key]['False Positive'], 
            full_cat_confusion[key]['False Negative'], 
            0, 0)
	del s['One Label Score']
	del s['Perfect Match Score']
	cat_stats.append({'Category': key,
			**full_cat_confusion[key], **s})

keys = full_res.keys()
with open(output_name, 'w') as f:
    d_write = csv.DictWriter(f, keys)
    d_write.writeheader()
    d_write.writerows([full_res])

keys = cat_stats[0].keys()
with open('results/by_cat.csv', 'w') as f:
    d_write = csv.DictWriter(f, keys)
    d_write.writeheader()
    d_write.writerows(cat_stats)

if save:
	clas.train(full_text, full_cat)
	clas.save_classifier()

