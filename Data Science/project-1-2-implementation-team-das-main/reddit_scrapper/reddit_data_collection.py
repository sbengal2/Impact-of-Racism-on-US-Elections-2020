import datetime

import pymongo
import requests

## this  script is used to collect the reddit data
# The subreddits are extracted from reddit
#search the for comments from the subreddits pulled and save this data in the database

my_client = pymongo.MongoClient("mongodb://localhost:27017/")
my_data_base = my_client["myDb"]
my_collection = my_data_base["redditCommentsNew"]

client_secret = "NKFqAojQx2LQZt6tVfNi19MygZo"

client_id = "ceTqOPa6fbwl3Q"
user_agent = "DataScience581"
username = "darshanVishnu"
password = "datascience580@2020"

base_url = 'https://www.reddit.com/'
data = {'grant_type': 'password', 'username': username, 'password': password}
auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
api_url = 'https://oauth.reddit.com'
headers = {}

#func used to get the bearer tocken
def validate():
    bearer_response = requests.post(base_url + 'api/v1/access_token',
                                    data=data,
                                    headers={'user-agent': 'DataScience581'},
                                    auth=auth)
    if bearer_response.status_code == 200:
        bearer_details = bearer_response.json()
        # print(bearer_details)
        token = 'bearer ' + bearer_details['access_token']
        # headers = {'Authorization': token, 'User-Agent': user_agent}
        headers['Authorization'] = token
        headers['User-Agent'] = user_agent
        response = requests.get(api_url + '/api/v1/me', headers=headers)
        return response.status_code == 200

# check for valid bearer token and pulls subreddits and pulls comments for eeach of the subreddits
def get_all_of_it():
    if validate() is True:
        get_all_subs()
        get_all_comments()

#used to prettyify data object
def pretty_time(created_utc):
    from datetime import datetime
    return datetime.fromtimestamp(created_utc).strftime("%Y-%m-%d %H:%M:%S")


id_list = []


# Function used to check the tree like structure in the comment data and extract the comments and put to the data base
def find_trees(x, subreddit_in, index_x, index_children):
    if len(x) <= index_x:
        return

    if x[index_x].get('data').get("children") is None:
        if record_present(x[index_x].get('data').get('id')):
            my_dict = {"subReddits": subreddit_in,
                       "comments": x[index_x].get('data').get('body'),
                       "created_utc": pretty_time(x[index_x].get('data').get('created_utc')),
                       "time": datetime.datetime.now(),
                       "comment_id": x[index_x].get('data').get('id')
                       }
            my_collection.insert_one(my_dict)
        find_trees(x, subreddit_in, index_x + 1, index_children)
    else:
        find_trees(x[index_x].get('data').get('children'), subreddit_in, 0, 0)


all_subreddits = []
all_ids = []

# pulls all the subreddits form the matching keywords 
def get_all_subs():
    query = (
            'politics' or 'USpolitics' or 'trump vs biden' or '2020Elections' or 'Racism'
            or 'george floyd' or 'Donald Trump' or 'Joe Biden' or '#WhatMatters2020' or '#blacklivesmatter'
            or 'black community' or 'us elections 2020' or 'Election2020' or 'AskAnAmerican' or 'Ask_Politics' or 'POLITIC'
            or 'PoliticalDiscussion' or 'Democrats' or 'Republican' or 'BlackPeopleTwitter' or 'The_Donald' or 'politics_new')
    payload = {'q': query, 'limit': 100, 'sort': 'relevance' or 'top' or 'new' or 'hot', 'type': 'sr'}
    subreddit_response = requests.get(api_url + '/search/',
                                      headers=headers, params=payload)
    if subreddit_response.status_code == 200:
        values = subreddit_response.json()
        for i in range(len(values['data']['children'])):
            all_subreddits.append(values['data']['children'][i]['data']['display_name'])
            all_ids.append(values['data']['children'][i]['data']['name'])

#pulls all the comments from the subreddit passed
def get_all_comments():
    # global count
    for sub_reddit in all_subreddits:
        comments_response = requests.get(api_url + '/r/' + sub_reddit + '/comments/', headers=headers)
        if comments_response.status_code == 200:
            values = comments_response.json()
            if values.get('data') is not None:
                val = values.get('data').get('children')
                print('Fetching comments from ' + sub_reddit + '.......\r', end='', flush=True)
                find_trees(val, sub_reddit, 0, 0, )
    all_subreddits.clear()

#check for the record present in the data base or not
def record_present(comment_id):
    return my_collection.count_documents({"comment_id": comment_id}, limit=1) == 0


