import sys
sys.path.insert(0, './data_files_scripts')

from Classify_with_evaluation import Classify
from data_files_scripts.MongoCollection import MongoCollection
from sklearn.model_selection import train_test_split
import numpy as np
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

print(len(text_dict))
print(len(cat_dict))

full_text = list()
full_cat = list()
for id in (sorted(text_dict.keys())):
	full_text.append(text_dict[id])
	full_cat.append(cat_dict[id])

print(len(full_text))
print(len(full_cat))

text_train, text_test, cat_train, cat_test = train_test_split(full_text, full_cat, 
	test_size = .2)

print(len(text_train))
print(len(text_test))
print(len(cat_train))
print(len(text_test))

cat_test_arr = np.array(cat_test, dtype=np.float64)
print(cat_test_arr)
print(sum(cat_test_arr))

clas = Classify(cat_train, text_train, 500)
predict = clas.predict(text_test)
#clas.evaluation_(cat_test,predict)
clas.simple_evaluation(cat_test,predict)

print(type(cat_test_arr))
print(type(predict))
print(cat_test_arr.shape)
print(predict.shape)
print(type(cat_test_arr[0][0]))
print(type(predict[0][0]))