from DB import DB
from Reader import Reader
from twitter_api import twitter_api
from MongoCollection import MongoCollection
import json

traincollection = MongoCollection()
trainlabelid=traincollection.return_ids_list()
Tweet=MongoCollection('Tweets')

dic={}
for id in trainlabelid:
    dic.setdefault(id,[]).append([[traincollection.return_catmatrix_by_id(id)]])#Tweet.return_tokenizers_by_id(id)
print('total documents:'+repr(len(dic)))







