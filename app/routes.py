import sys
sys.path.insert(0, '..')

from flask import request, jsonify, render_template
from app import app
import json
import urllib.request
import app.search_rest as rest

# Tweets variable to store all retrieved tweets by the Twitter API.
tweets = None
# Tooltips to explain different classes, shown when class elements are hovered.
tooltips = {'GoodsServices':'The user is asking for a particular service or physical good.', 'SearchAndRescue':'The user is requesting a rescue (for themselves or others)',
            'InformationWanted':'The user is requesting information', 'CallToAction':'The user is asking people to volunteer to help the response effort',
            'Donations':'The user is asking people to donate goods/money','MovePeople':'The user is asking people to leave an area or go to another area',
            'FirstPartyObservation':'The user is giving an eye-witness account','ThirdPartyObservation':'The user is reporting a information that they recieved from someone else',
            'Weather':'The user is providing a weather report (current or forcast)','EmergingThreats':'The user is reporting a potential problem that may cause future loss of life or damage',
            'SignificantEventChange':'The user is reporting a new occurence that public safety officers need to respond to.', 'MultimediaShare':'The user is sharing images or video',
            'ServiceAvailable':'The user is reporting that they or someone else is providing a service', 'Factoid':'The user is relating some facts, typically numerical',
            'Official':'An official report by a government or public safety representative', 'CleanUp':'A report of the clean up after the event',
            'Hashtags':'Reporting which hashtags correspond to each event', 'PastNews':'The post is generic news, e.g. reporting that the event occured',
            'ContinuingNews':'The post providing/linking to continious coverage of the event', 'Advice':'The author is providing some advice to the public',
            'Sentiment':'The post is expressing some sentiment about the event', 'Discussion':'Users are discussing the event',
            'Irrelevant':'The post is irrelevant, contains no information', 'Unknown':'Does not fit into any other category',
            'KnownAlready':'The Responder already knows this information'}


# Home and index page.
@app.route('/')
@app.route('/home')
def home():
        return render_template('home.html', title='Home', search= True)


# Filter functions.
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


# Add HTML of tweets to a grid with pagination.
def beautify_html(tweets):
    data_page = 1
    html = '<div class="pagination-container"><div data-page="1"><div class="row">'

    # Loop over HTML of tweets and add to grid of two columns.
    for i in range(0, len(tweets)):
        if i == len(tweets) - 1:
            html += '<div class="col-sm">' + tweets[i]['html'] + '</div>'
            html += '</div></div>'
            break

        # After 20 tweets, add new page.
        if i % 20 == 0  and i != 0:
            data_page += 1
            html += '</div></div><div data-page="' + str(data_page) + '" style="display:none;"><div class="row">'

        # Create new row when two columns are added.
        if i % 2 == 0 and i != 0 and i % 20 != 0:
            html += '</div><div class="row">'

        # Add tweet HTML to column.
        html += '<div class="col-sm">' + tweets[i]['html'] + '</div>'

    # Add page numbers to bottom of grid.
    html += """<div class="text-center">
                <div class="pagination pagination-centered">
                  <ul class="pagination ">
                    <li data-page="-" ><a href="#" class="page-link">&lt;</a></li>
                    <li data-page="1"><a href="#" class="page-link">1</a></li>"""

    for i in range(2, data_page + 1):
        html += '<li data-page="' + str(i) + '"><a href="#" class="page-link">' + str(i) + '</a></li>'

    html += """     <li data-page="+"><a href="#" class="page-link">&gt;</a></li>
                   </ul>
                  </div>
                 </div>
                </div>"""

    return html


# Filter tweets based on active categories and active filters set by the user.
@app.route('/filter_tweets')
def filter_tweets():
    global tweets
    # Create a local copy of all tweets. This is needed because we will return a portion of all tweets because of the filters used.
    # When a user will change the filters later on, we can just use a copy of all tweets again.
    tweets_copy = tweets.copy()
    # Get active categories and filters.
    active_filters = request.args.get('filters').split(',')
    active_categories = request.args.get('categories').split(',')
    chronological = request.args.get('chronological')

    # Dict linked to functions above to reduce syntax.
    filters = {'media-yes' : media_yes,
               'media-no' : media_no,
               'priority-high' : priority_high,
               'priority-medium' : priority_medium,
               'priority-low' : priority_low
    }

    # Loop over all tweets and add tweet to new tweets when criteria are met.
    new_tweets = []
    for tweet in tweets_copy:
        # Check if tweet contains one of the active categories.
        if not set(tweet['Category']).isdisjoint(active_categories):
            tweet_filters = []

            # Check for each filter if the tweet will be showed to the user.
            for active_filter in active_filters:
                tweet_filters.append(filters[active_filter](tweet))

            # Tweet can have priority: low or medium or high and media: yes or no.
            # When 2 of 5 filters are set to True: add to new tweets.
            if tweet_filters.count(True) == 2:
                new_tweets.append(tweet)

    # Order new filtered tweets based on the order filter.
    if chronological == 'true':
        new_tweets = order_chronological(new_tweets)
    else:
        new_tweets = order_reverse_chronological(new_tweets)

    # Add HTML of tweets to grid with pagination.
    return beautify_html(new_tweets)


# Method to retrieve tweets when user submitted query + number of tweets.
@app.route("/search", methods= ['POST'])
def search():
    global tweets
    global tooltips
    # Get form inputs.
    query= request.form['query']
    tweet_num= request.form['tweet_num']
    try:
        # Get tweets from Twitter API along with categories.
        tweets, tweetids, categories = rest.query_search(query, tweet_num)
    except Exception:
        return render_template('home.html', error=True)
    # Loop over retrieved tweets to get corresponding HTML.
    for tweet in tweets:
            try:
                # Get embedded HTML from Twitter API to make tweets pretty.
                url= 'https://publish.twitter.com/oembed?url=https://twitter.com/anybody/status/'+ tweet['Postid'] + '?maxwidth=220'
                response = urllib.request.urlopen(url)
                data = json.load(response)
                tweet['html'] = data['html']
            except:
                continue
    
    # Order tweets.
    tweets = order_chronological(tweets)
    # Add HTML of tweets to grid with pagination.
    html = beautify_html(tweets.copy())
    return render_template('form.html', tweets=html, categories=categories, tooltips=tooltips, tweet_num=tweet_num, query= query) 


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404
