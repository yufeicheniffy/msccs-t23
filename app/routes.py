from flask import request, jsonify, render_template
from app import app
from classifier.data_files_scripts import MongoCollection
from app.searchForm import searchForm
import json
from bson import json_util, ObjectId
import app.search_rest as rest

@app.route('/')
@app.route('/index') #home and index page.
def home():
        user = {'username': 'Team28'}
        return render_template('index.html', title='Home', user=user)

@app.route('/tweetapi', methods=['GET'])# a route to call tweet api,by a seatch form
def tweetapi():
    return render_template('form.html')

@app.route('/RequestForms')# a route to recieve retieve condition
def RequestForms():
    form = searchForm()
    return render_template('forms.html', title='Request Tweets', form=form)

@app.route('/searchresults')# a route to show Tweet content
def results():
        database=MongoCollection.MongoCollection(collectionname='Training_token')
        Tweets={
        'PostID':"243374590288592896",
        'text':database.find_text_by_id("243374590288592896"),
        'catagories':database.find_category_by_id("243374590288592896"),
        'priority':database.return_priority_by_id("243374590288592896")
        }
        return render_template('searchresults.html',title='Results',Tweets=Tweets)

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404
    
@app.route('/api/v1/resources/', methods=['GET']) # return the result of tweetapi.
def api_all():
        # run locally http://127.0.0.1:5000/api/v1/resources/
        # will return a json result of the first 100 Test data, you can change the limit
    mycol = MongoCollection.MongoCollection(collectionname='Test')
    results=[]
    for tweet in mycol.return_collection().find().limit(int(100)):
        results.append(json.loads(json_util.dumps(tweet)))

    return (jsonify(results))

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
    # use the name that you gave to your collection
    mycol = MongoCollection.MongoCollection(collectionname='func_test')
    results, ids = rest.query_search(query)
    mycol.return_collection().insert(results)
    return jsonify({"name": ids})