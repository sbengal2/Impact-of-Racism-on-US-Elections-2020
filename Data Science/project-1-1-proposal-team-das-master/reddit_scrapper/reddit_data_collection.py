import requests
import pymongo
import datetime

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["myDb"]
mycol = mydb["redditData3"]

client_secret = "NKFqAojQx2LQZt6tVfNi19MygZo"

client_id = "ceTqOPa6fbwl3Q"
user_agent = "DataScience581"
username = "darshanVishnu"
password = "datascience580@2020"

base_url = 'https://www.reddit.com/'
data = {'grant_type': 'password', 'username': username, 'password': password}
auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
r = requests.post(base_url + 'api/v1/access_token',
                  data=data,
                  headers={'user-agent': 'DataScience581'},
                  auth=auth)
d = r.json()
# print(d)
token = 'bearer ' + d['access_token']

api_url = 'https://oauth.reddit.com'

headers = {'Authorization': token, 'User-Agent': user_agent}
response = requests.get(api_url + '/api/v1/me', headers=headers)


# if response.status_code == 200:
# print(response.json()['name'], response.json()['comment_karma'])

# print(r.status_code)


def findTress(x, subredditsIn, index_x, index_children):
    if (len(x) <= index_x):
        return

    if (x[index_x].get('data').get("children") == None):
        mydict = {}

        # print(x[index_x].get('data').get('body'))
        mydict["subReddits"] = subredditsIn
        mydict["comments"] = x[index_x].get('data').get('body')
        mydict["time"] = datetime.datetime.now()
        mycol.insert_one(mydict)
        return findTress(x, subredditsIn, index_x + 1, index_children)
    else:
        # listComments.append(x.get('data').get('children'))
        return findTress(x[index_x].get('data').get('children'), subredditsIn, 0, 0)


query = ('politics' or 'uspolitics' or 'trump vs biden' or '2020Elections' or 'black lives matter' or 'george floyd')
payload = {'q': query, 'limit': 100, 'sort': 'top', 'type': 'sr'}
response = requests.get(api_url + '/search/',
                        headers=headers, params=payload)

# print(response.status_code)

values = response.json()
# print(response.text)

# #
# print(values.keys())
listdisplayname = []
listdisct = {}
for i in range(len(values['data']['children'])):
    listdisplayname.append(values['data']['children'][i]['data']['display_name'])
    listdisct["date"] = listdisplayname
    # print(values['data']['children'][i]['data']['display_name'])

#     print("####")
#     x = mycol.insert_one(values['data']['children'][i]['data'])


print(listdisplayname)

for subreddits in listdisplayname:
    response1 = requests.get(api_url + '/r/' + subreddits + '/comments/', headers=headers)
    values = response1.json()
    # print(values)
    if values.get('data') is not None:
        val = values.get('data').get('children')
        findTress(val, subreddits, 0, 0, )
