import sys
sys.path.insert(0, './data_files_scripts')
sys.path.insert(0, './classifier')

from Classify_with_evaluation import Classify
from data_files_scripts.MongoCollection import MongoCollection
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
import csv

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
full_res = list()

k = [1, 5, 10, 25]
weights = ['uniform', 'distance']

for k, weight in [(x, y) for x in k for y in weights]:

	model_res = {'Number of Predictions': 0, 'True Positive': 0,
				'True Negative': 0, 'False Positive': 0,
				'False Negative': 0, 'One Label': 0,
				'Perfect Match': 0}

	for event in set(event_dict.values()):
		test_rows = np.argwhere(full_event == event)
		train_rows = np.argwhere(full_event != event)
		
		text_test = [full_text[n[0]] for n in test_rows]
		cat_test = [full_cat[n[0]] for n in test_rows]
		
		text_train = [full_text[n[0]] for n in train_rows]
		cat_train = [full_cat[n[0]] for n in train_rows]

		cat_test_arr = np.array(cat_test, dtype=np.float64)
		clas = Classify(text_train, cat_train, 1000, 
			model = KNeighborsClassifier(n_neighbors = k, 
				weights = weight, n_jobs = 2))

		predict = clas.predict(text_test)
		simp = clas.simple_evaluation(cat_test, predict)

		for key in simp:
			if key in model_res:
				model_res[key] += simp[key]

	stats = clas.stats_calc(model_res['True Positive'], 
	            model_res['True Negative'], model_res['False Positive'], 
	            model_res['False Negative'], model_res['One Label'], 
	            model_res['Perfect Match'])

	model_res = {**model_res, **stats, 'K': k, 'weight': weight}
	print("\n\nModel Results: ")
	for key in model_res:
			print(key, ": ", model_res[key])
	full_res.append(model_res)

keys = full_res[0].keys()
with open('results/knn_param_results.csv', 'w') as f:
    dict_writer = csv.DictWriter(f, keys)
    dict_writer.writeheader()
    dict_writer.writerows(full_res)
