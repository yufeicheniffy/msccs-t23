from Classify_with_evaluation import Classify
import pymongo

# runs locally
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
# input your database name
mydb = myclient["MasterProject"]
mycol = mydb["Test"]
ytest = []
xtest = []

#for computation reasons just test TWICE the first ytest works with all the TestCollection
i=0
for tweet in mycol.find():


	x_ = tweet["text"]
	print(tweet)
	if('categories' in tweet):
		y_ = tweet["categories"]
	else:
		y_ = tweet["categories "]
	ytest.append(y_)
	xtest.append(x_)
print("YTEST")
print(ytest)

clas = Classify()
clas.train()
predict = clas.predict(xtest)
#returns a csv file with a dataframe
clas.evaluation_(ytest,predict )
