from flask import request, jsonify, render_template
from app import app
from classifier.data_files_scripts import MongoCollection
from app.searchForm import searchForm
import json
import urllib.request
from bson import json_util, ObjectId
import app.search_rest as rest
#from classifier.test_classifier_with_evaluation import clas

G_collection=None #the instance of MongoCollection, Don't need to create a lot of instance.
tweets = None


def initdatabase(): #!!!!A function to ensure the database is connected. Add this in EVERY routes function please.
        global G_collection
        if G_collection is None:
                G_collection=MongoCollection.MongoCollection(MongoURI="mongodb://localhost:27017/", collectionname='TweetsData')#MongoURI="mongodb://localhost:27017/"
                 #create the instance in the home page. Each time the project should run start with home page.
        else:
                return

@app.route('/')
@app.route('/home') #home and index page.
def home2():
        initdatabase()
        return render_template('home.html', title='Home', search= True)

# def remove_html(postids):
#     global results
#     global tweetids
#     global categories
#     global html_tweets
#     new_html = []
#     for html_tweet in html_tweets:
#         for postid in postids:
#             if postid in html_tweet:
#                 new_html.append(html_tweet)
#                 break

#     return new_html

def media_yes(tweet):
    return tweet['Media']

def media_no(tweet):
    return not tweet['Media']

def priority_low(tweet):
    return tweet['Priority'] == 'Low'

def priority_medium(tweet):
    return tweet['Priority'] == 'Medium'

def priority_high(tweet):
    return tweet['Priority'] == 'High'

def order_chronological(tweets):
    return sorted(tweets, key=lambda k: k['timestamp'], reverse=True) 

def order_reverse_chronological(tweets):
    return sorted(tweets, key=lambda k: k['timestamp']) 


def beautify_html(tweets):
    html = '<div class="row">'

    for i in range(0, len(tweets)):
        if i == len(tweets) - 1:
            html += '</div>'
            break

        if i % 2 == 0 and i != 0:
            html += '</div><div class="row">'

        html += '<div class="col-sm">' + tweets[i]['html'] + '</div>'

    return html


@app.route('/filter_tweets')
def filter_tweets():
    global tweets
    tweets_copy = tweets.copy()
    active_filters = request.args.get('filters').split(',')
    active_categories = request.args.get('categories').split(',')
    chronological = request.args.get('chronological')

    filters = {'media-yes' : media_yes,
               'media-no' : media_no,
               'priority-high' : priority_high,
               'priority-medium' : priority_medium,
               'priority-low' : priority_low
    }

    new_tweets = []
    for tweet in tweets_copy:
        if not set(tweet['Category']).isdisjoint(active_categories):
            tweet_filters = []

            for active_filter in active_filters:
                tweet_filters.append(filters[active_filter](tweet))

            if tweet_filters.count(True) == 2:
                new_tweets.append(tweet)

    if chronological == 'true':
        new_tweets = order_chronological(new_tweets)
    else:
        new_tweets = order_reverse_chronological(new_tweets)


    return beautify_html(new_tweets)


@app.route("/search", methods= ['POST'])
def search():
        global tweets
        #first to collect a query from front-end and store in a variable
        query= request.form['query']
        tweet_num= request.form['tweet_num']
        print('here',query,tweet_num)
        # use the name that you gave to your collection
        try:
                database=G_collection.set_collection(collectionname='TweetsData')
        except:
                return render_template('databaseerrorpage.html', search= True)
        try:
                tweets, tweetids, categories = rest.query_search(query, tweet_num)
        except Exception:
                return render_template('searcherrorpage.html', search= True)
        # query the db based on the query from front-end
        for tweet in tweets:
                # building the url to use for the http get request
                url= 'https://publish.twitter.com/oembed?url=https://twitter.com/anybody/status/'+ tweet['Postid'] + '?maxwidth=220'
                # using the get request
                response = urllib.request.urlopen(url)
                print(response)
                data = json.load(response)
                tweet['html'] = data['html']

                # some ids get back empty because maybe the tweet is deleted, so only get json if true
                # if page:
                # #return the response of the get request in json form
                #         tweet= page.json()
                #         # target the field html from the json response
                #         tweet_tag= tweet['html']
                #         print(tweet_tag)
                #         #append all the html responses to a list to make to loop with in the html
                #         tweet_html.append(tweet_tag)
        
        tweets = order_chronological(tweets)
        print(tweets)
        return render_template('form.html', tweets=tweets, categories=categories, tweet_num=tweet_num, query= query) 


@app.route('/tweetapi', methods=['GET', 'POST'])# a route to call tweet api,by a seatch form
def tweetapi():
        initdatabase()
        return render_template('form.html')

@app.route('/RequestForms')# a route to recieve retieve condition
def RequestForms():
        initdatabase()
        form = searchForm()
        return render_template('forms.html', title='Request Tweets', form=form)

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

@app.route('/api/v1/resources/', methods=['GET']) # return the result of tweetapi.
def api_all():
        # run locally http://127.0.0.1:5000/api/v1/resources/
        # will return a json result of the first 100 Test data, you can change the limit
        initdatabase()
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
        initdatabase()
        query= request.form['query']
        # use the name that you gave to your collection
        database=G_collection.set_collection(collectionname='TweetsData')
        try:
                results, ids,dic_cates = rest.query_search(query)
                database.insert(results)
        except Exception:
                print('no result found!')
                return render_template('errorpage.html')
        return jsonify({"name": ids})

@app.route('/priority_html', methods=['GET'])# a route to call tweet api,by a seatch form
def priotiy_html():
        initdatabase()
        return render_template('form_by_priority.html')

@app.route('/priority', methods=['POST'])
def api_filter_priority():
        initdatabase()
        priority= request.form['priority']
        print(priority)
        # use the name that you gave to your collection
        G_collection.set_collection(collectionname='TweetsData')
        ids = G_collection.return_tweets_by_priority(priority)

        return jsonify({"name": len(ids)})

@app.route('/category_html', methods=['GET'])# a route to call tweet api,by a seatch form
def category():
        initdatabase()
        return render_template('category.html')

@app.route('/category_filter', methods=['POST'])
def api_filter_category():
        initdatabase()
        category= request.form['category']
        print(category)
        # use the name that you gave to your collection
        G_collection.set_collection(collectionname='TweetsData')
        ids = G_collection.return_tweets_by_category(category)
        #text= G_collection.find_text_by_ids(ids)

        return jsonify({"name": len(ids)})

@app.route('/eventfilter_html', methods=['GET'])# a route to call tweet api,by a seatch form
def event():
        initdatabase()
        return render_template('eventfilter_html')

@app.route('/eventfilter', methods=['POST'])
def api_filter_event():
        initdatabase()
        event= request.form['eventfilter']
        print(event)
        # use the name that you gave to your collection
        G_collection.set_collection(collectionname='TweetsData')
        ids = G_collection.return_tweets_by_event(event)
        #text= G_collection.find_text_by_ids(ids)

        return jsonify({"name": len(ids)})
