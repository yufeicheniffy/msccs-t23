import flask
from flask import request, jsonify, render_template
import pymongo
import json
from bson import json_util, ObjectId
import search_rest as rest


app = flask.Flask(__name__)
app.config["DEBUG"] = True




@app.route('/', methods=['GET'])
def home():
    return render_template('form.html')


# run locally http://127.0.0.1:5000/api/v1/resources/
# will return a json result of the first 100 Test data, you can change the limit
@app.route('/api/v1/resources/', methods=['GET'])
def api_all():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["MasterProject"]
    mycol = mydb["Test"]
    results=[]
    for tweet in mycol.find().limit(int(100)):
        results.append(json.loads(json_util.dumps(tweet)))

    return (jsonify(results))





@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


#0 Post method which means that our method is waiting for an input.
#1 we retrieve this input by ajax call and request from the form that our html file has.
#2 we do a search query at twitter api with the help of search_rest script (as rest)
#3 we save the real events result at a db and we return to the Html/javascript page a list of ids
#4 in order to be easy to visualise
#5 we can classify the real event tweets and then store them at the DB:
# Just run  the api.py and run to your local browser at the ip that your cmd shows
# you must set a local database with the guide of Yufei in order to run this
#cheers
@app.route('/process', methods=['POST'])
def api_filter():
    query= request.form['query']
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    #use the name that you gave to your db
    mydb = myclient["MasterProject"]
    # use the name that you gave to your collection
    mycol = mydb["real_events"]
    results, ids = rest.query_search(query)
    mycol.insert(results)
    return jsonify({"name": ids})




app.run()
