from DB import DB
from Reader import Reader
from twitter_api import twitter_api
from MongoCollection import MongoCollection
import json
import sys
import io


sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') 

traincollection = MongoCollection(collectionname='Test', MongoURI="mongodb://localhost:27017/")
read=Reader()
l1=read.read('''./classifier/data_files_scripts/data_files/ssr1.json''')
l2=read.read('''./classifier/data_files_scripts/data_files/ssr2.json''')
l3=read.read('''./classifier/data_files_scripts/data_files/ssr3.json''')
l4=read.read('''./classifier/data_files_scripts/data_files/ssr4.json''')
l5=read.read('''./classifier/data_files_scripts/data_files/ssr5.json''')
l6=read.read('''./classifier/data_files_scripts/data_files/ssr6.json''')
traincollection.insert(l1)
traincollection.insert(l2)
traincollection.insert(l3)
traincollection.insert(l4)
traincollection.insert(l5)
traincollection.insert(l6)
#ids=[]
#event=[]
#for i in range(0,len(l)):
#    ids.append(l[i]["postID"])
#    event.append(l[i]["event"])

#traincollection.updata_event_by_ids(ids,event)


#with open('''.\classifier\data_files_scripts\data_files\TRECIS-CTIT-H-Training.json''', encoding="utf8") as json_data:
#    data = json.load(json_data)
#    dic=data["events"][1]["tweets"]
#    dic[1]['event']=data["events"][1]["eventid"]
#    print(data["events"][1]["eventid"])
#    print(len(dic))

#traincollection.updata_category_by_id("266222386045661184",["Factoid","ContinuingNews","testcate"])
#traincollection.updata_event_by_ids(["266222386045661184"],"italyearthquake")
#print(traincollection.find_category_by_id("266222386045661184"))
#print(traincollection.return_event_by_id("266222386045661184"))
#trainlabelid=traincollection.return_ids_list()
#dic=traincollection.return_classfier_dic()
#print(dic)
#print(repr(len(trainlabelid))+'--ok')
#coll=MongoCollection('Training_token')
#coll.find_text_by_id('243374590288592896')
#coll.return_train_dic()
#Tweet=MongoCollection('Tweets')
#dic={}
#for id in trainlabelid:
#   dic.setdefault(id,[]).append([[traincollection.return_catmatrix_by_id(id)]])#Tweet.return_tokenizers_by_id(id)
#print('total documents:'+repr(len(dic)))
#twitter=twitter_api("IHpSjYd5AuCdDRZTaGiMOwHUJ", "FNUvxez9N9vBzY72HiZcukHQqVqO0ZiV498qyaYDxaV5nKFSgu",traincollection)
#coll.insert(twitter.list_from_ids(trainlabelid))







