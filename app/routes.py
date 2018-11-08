from flask import render_template
from app import app
from classifier.data_files_scripts import MongoCollection
from app.searchForm import searchForm

@app.route('/')
@app.route('/index')
def home():
        user = {'username': 'Team28'}
        return render_template('index.html', title='Home', user=user)

@app.route('/RequestForms')
def RequestForms():
    form = searchForm()
    return render_template('forms.html', title='Request Tweets', form=form)

@app.route('/searchresults')
def results():
        database=MongoCollection.MongoCollection(collectionname='Training_token')
        Tweets={
        'PostID':"243374590288592896",
        'text':database.find_text_by_id("243374590288592896"),
        'catagories':database.find_category_by_id("243374590288592896"),
        'priority':database.return_priority_by_id("243374590288592896")
        }
        return render_template('searchresults.html',title='Results',Tweets=Tweets)