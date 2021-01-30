import pymongo
from flask import Flask, render_template, redirect, url_for, request
from flask_pymongo import PyMongo
from database import *
app = Flask(__name__)

# local
app.config["MONGO_URI"] = "mongodb://localhost:27017/myDb"
mongo = PyMongo(app)
twitter_collection = mongo.db.twitter_test
reddit_collection = mongo.db.reddit_test
hashtag_count = {}
date_count = {}


# Index
@app.route('/')
def index():
    return render_template('home.html')


@app.route('/about')
def about_us():
    return render_template('about.html')


@app.route('/popular_hashtags', methods=['GET', 'POST'])
def popular_hashtags():
    global hashtag_count
    if request.method == 'POST':
        topic = request.form['topic']
        if len(topic) == 0:
            error = 'Please enter a topic'
            return render_template('hashtag.html', error=error)
        else:
            hashtag_count = start(topic, twitter_collection)
            return redirect(url_for('hashtag_bar'))
    return render_template('hashtag.html')


@app.route('/data_by_date', methods=['GET', 'POST'])
def tweet_by_date():
    global date_count
    if request.method == 'POST':
        source = request.form['source']
        from_date = request.form['from']
        to_date = request.form['to']
        if len(from_date) == 0 or len(to_date) == 0:
            error = 'Please enter start and end dates'
            return render_template('date.html', error=error)
        else:
            if str(source) == 'twitter':
                date_count = get_by_date(from_date, to_date, twitter_collection, str(source))
                if date_count is None:
                    error = 'Please check the date format'
                    return render_template('date.html', error=error)
                else:
                    return redirect(url_for('twitter_dates'))
            else:
                date_count = get_by_date(from_date, to_date, reddit_collection, str(source))
                if date_count is None:
                    error = 'Please check the date format'
                    return render_template('date.html', error=error)
                else:
                    return redirect(url_for('reddit_dates'))
    return render_template('date.html')


@app.route('/hashtag_bar')
def hashtag_bar():
    if bool(hashtag_count) == False:
        error = 'No hashtags found'
        return render_template('bar.html', error=error)
    else:
        labels = hashtag_count.keys()
        values = hashtag_count.values()
        bar_labels = labels
        bar_values = values
        return render_template('bar.html', title='Number of hashtags by search term', max=max(values),
                               labels=bar_labels,
                               values=bar_values)


@app.route('/twitter_date_graph')
def twitter_dates():
    if bool(date_count) == False:
        error = 'No data found for the entered dates'
        return render_template('bar.html', error=error)
    else:
        labels = date_count.keys()
        values = date_count.values()
        bar_labels = labels
        bar_values = values
        return render_template('line.html', title='Number of tweets collected from twitter by date', max=max(values),
                               labels=bar_labels,
                               values=bar_values)


@app.route('/reddit_date_graph')
def reddit_dates():
    if bool(date_count) == False:
        error = 'No data found for the entered dates'
        return render_template('bar.html', error=error)
    else:
        labels = date_count.keys()
        values = date_count.values()
        bar_labels = labels
        bar_values = values
        return render_template('line.html', title='Number of comments collected from reddit by date', max=max(values),
                               labels=bar_labels,
                               values=bar_values)


if __name__ == '__main__':
    app.run(debug=True)
