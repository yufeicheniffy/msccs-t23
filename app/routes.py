from flask import request, jsonify, render_template
from app import app
from classifier.data_files_scripts import MongoCollection
from app.searchForm import searchForm
import json
from bson import json_util, ObjectId
import app.search_rest as rest


global G_collection #the instance of MongoCollection, Don't need to create a lot of instance.


@app.route('/')
def home():
        global G_collection
        G_collection=MongoCollection.MongoCollection(collectionname='TweetsData') #create the instance in the home page. Each time the project should run start with home page.
        user = {'username': 'Team28'}
        return render_template('index.html', title='Home', user=user)

@app.route('/index') #home and index page.
def index():
        global G_collection
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
        database=G_collection.set_collection(collectionname='TweetsData')
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
    database=G_collection.set_collection(collectionname='TweetsData')
    results=[]
    for tweet in database.collection.find().limit(int(100)):
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
    database=G_collection.set_collection(collectionname='Test_Panos')
    results, ids = rest.query_search(query)
    database.insert(results)
    return jsonify({"name": ids})

@app.route('/priority_html', methods=['GET'])# a route to call tweet api,by a seatch form
def priotiy_html():
    return render_template('form_by_priority.html')

@app.route('/priority', methods=['POST'])
def api_filter_priority():
    priority= request.form['priority']
    print(priority)
    # use the name that you gave to your collection
    G_collection.set_collection(collectionname='TweetsData')
    ids = G_collection.return_tweets_by_priority(priority)

    return jsonify({"name": len(ids)})

@app.route('/category_html', methods=['GET'])# a route to call tweet api,by a seatch form
def category():
    return render_template('category.html')

@app.route('/category_filter', methods=['POST'])
def api_filter_category():
    category= request.form['category']
    print(category)
    # use the name that you gave to your collection
    G_collection.set_collection(collectionname='TweetsData')
    ids = G_collection.return_tweets_by_category(category)

    return jsonify({"name": len(ids)})
