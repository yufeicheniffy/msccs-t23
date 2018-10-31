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
ytest.append(mycol.find_one()["categories"])
ytest.append(mycol.find_one()["categories"])
xtest.append(mycol.find_one()["text"])
xtest.append(mycol.find_one()["text"])
print("YTEST")
print(ytest)

clas = Classify()
clas.train()
predict = clas.predict(xtest)
#returns a csv file with a dataframe
clas.evaluation_(ytest,predict )
