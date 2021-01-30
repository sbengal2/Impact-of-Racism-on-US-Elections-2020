import re
import pandas as pd

tweet_list = []

def to_lower_case(tweet):
    return tweet.lower()

def trump_tweets(tweet):
    key_words = ["donald trump","trump","donald","ivanka","@realdonaldtrump","@potus","#maga","maga","trump wall","republicans",
                 "#trump2020landside","melania","#donaldtrump","#trump","#donald","#ivanka","#trumpwall","#republicans","#trump2020landside","#melania",
                 "mexicans","wall","the donald","donald j. trump","trump news","trump twitter","president"]
    patterns = [r'\b%s\b' % re.escape(word.strip()) for word in key_words]
    regex = re.compile('|'.join(patterns))
    if regex.search(to_lower_case(str(tweet))):
        return True
    return False

def create_new_frame():
    for index, row in data.iterrows():
        if trump_tweets(row['tweets']):
            tweet_list.append(row['tweets'])

# data = pd.read_csv("/Volumes/My Passport/MongoData/final sets/racist_data_set.csv")
data = pd.read_csv("racist_data_set.csv")
create_new_frame()
new_data = pd.DataFrame(tweet_list,columns=['tweets'])
new_data.to_csv('trump_twitter_set.csv',index=True)