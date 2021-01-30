import re
import dateutil.parser


def get_tweets(tag, collection):
    tweet_list = []
    for x in collection.find():
        regex = re.compile(r"\b" + re.escape(tag) + r"\b", re.IGNORECASE)
        tweet = x['text']
        match = re.search(regex, str(tweet))
        if match is not None:
            tweet_list.append(str(tweet))
    return tweet_list


def clean_input(tag):
    tag = tag.replace(" ", "")
    if tag.startswith('#'):
        return tag[1:].lower()
    else:
        return tag.lower()


def return_all_hashtags(tweets):
    all_hashtags = []
    for tweet in tweets:
        for word in str(tweet).split():
            if word.startswith('#'):
                all_hashtags.append(word.lower())
    return all_hashtags


def get_hashtags(tag, collection):
    search_tag = clean_input(tag)
    tweets = get_tweets(search_tag, collection)
    all_tags = return_all_hashtags(tweets)
    frequency = {}
    for item in set(all_tags):
        frequency[item] = all_tags.count(item)
    return {k: v for k, v in sorted(frequency.items(),
                                    key=lambda item: item[1], reverse=True)}


def start(tag, collection):
    all_tags = get_hashtags(tag, collection)
    if len(all_tags) == 0:
        return {}
    else:
        top_five = dict(list(all_tags.items())[0: 5])
        return top_five


def get_by_date(start_date, end_date, collection, source):
    date_count = {}
    sorted_date_count = {}
    if source == 'twitter':
        try:
            start_date = dateutil.parser.parse(start_date)
            end = dateutil.parser.parse(end_date)
        except:
            return None
        doc = twitter_date(start_date, end, collection)
        for x in doc:
            d = x['_id']['new_date']
            v = x['count']
            date_count[d] = v
        for key in sorted(date_count.keys()):
            sorted_date_count[key] = date_count[key]
        return sorted_date_count
    elif source == 'reddit':
        try:
            start_date = dateutil.parser.parse(start_date)
            end = dateutil.parser.parse(end_date)
        except:
            return None
        doc = reddit_date(start_date, end, collection)
        for x in doc:
            d = x['_id']['new_date']
            v = x['count']
            date_count[d] = v
        for key in sorted(date_count.keys()):
            sorted_date_count[key] = date_count[key]
        return sorted_date_count


def twitter_date(start_date, end_date, collection):
    return collection.aggregate([{"$project": {"date": {"$dateFromString": {"dateString": "$date"}}}},
                                 {"$project": {"date": {"day": {"$dayOfMonth": '$date'}, "month": {"$month": "$date"},
                                                        "year": {"$year": '$date'}}}},
                                 {"$project": {"new_date": {
                                     "$dateFromParts": {"year": "$date.year", "month": "$date.month",
                                                        "day": "$date.day"}}}},
                                 {"$match": {"new_date": {"$lte": end_date, "$gte": start_date}}},
                                 {"$group": {"_id": {"new_date": '$new_date'}, "count": {"$sum": 1}}}
                                 ])


def reddit_date(start_date, end_date, collection):
    return collection.aggregate([{"$project": {"date": {"day": {"$dayOfMonth": '$time'}, "month": {"$month": "$time"},
                                                        "year": {"$year": '$time'}}}},
                                 {"$project": {"new_date": {
                                     "$dateFromParts": {"year": "$date.year", "month": "$date.month",
                                                        "day": "$date.day"}}}},
                                 {"$match": {"new_date": {"$lte": end_date, "$gte": start_date}}},
                                 {"$group": {"_id": {"new_date": '$new_date'}, "count": {"$sum": 1}}}
                                 ])
