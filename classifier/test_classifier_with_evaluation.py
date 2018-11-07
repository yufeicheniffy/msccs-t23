import sys
sys.path.insert(0, './data_files_scripts')

from Classify_with_evaluation import Classify
from data_files_scripts.MongoCollection import MongoCollection
from sklearn.model_selection import train_test_split
import numpy as np
import csv

# runs locally
training_connect = MongoCollection(collectionname='Training_token', MongoURI="mongodb://localhost:27017/")
test_connect = MongoCollection(collectionname='Test', MongoURI="mongodb://localhost:27017/")

#resplit train/test
td0 = training_connect.return_text_all()
cd0 = training_connect.return_catdict_all()
print(len(td0))
print(len(cd0))
td1 = test_connect.return_text_all()
cd1 = test_connect.return_catdict_all()
print(len(td1))
print(len(cd1))


text_dict = {**td0, **td1}
cat_dict = {**cd0, **cd1}

full_text = list()
full_cat = list()
for id in (sorted(text_dict.keys())):
	full_text.append(text_dict[id])
	full_cat.append(cat_dict[id])

text_train, text_test, cat_train, cat_test = train_test_split(full_text, full_cat, 
	test_size = .1)



cat_test_arr = np.array(cat_test, dtype=np.float64)

clas = Classify(cat_train, text_train, 2000)
predict = clas.predict(text_test)
evals = clas.evaluation_(cat_test,predict, sorted(training_connect.catadictionary, 
	key=training_connect.catadictionary.__getitem__))
clas.simple_evaluation(cat_test,predict)

keys = evals[0].keys()
with open('eval.csv', 'w') as f:
    d_write = csv.DictWriter(f, keys)
    d_write.writeheader()
    d_write.writerows(evals)

