import re
import pandas as pd

tweet_list = []

def to_lower_case(tweet):
    return tweet.lower()

def biden_tweets(tweet):
    key_words = ["joe","biden","joe biden","@joebiden","kamala","harris","kamala harris","obama","barack obama","democrats",
                 "#votebidenharristosaveamerica","#joebiden","#joe","#biden","#harris","#kamala","#democrats","#bidenharris",
                "president","asian woman","black woman","indian"]
    patterns = [r'\b%s\b' % re.escape(word.strip()) for word in key_words]
    regex = re.compile('|'.join(patterns))
    if regex.search(to_lower_case(str(tweet))):
        return True
    return False

def create_new_frame():
    for index, row in data.iterrows():
        if biden_tweets(row['tweets']):
            tweet_list.append(row['tweets'])

# data = pd.read_csv("/Volumes/My Passport/MongoData/final sets/racist_data_set.csv")
data = pd.read_csv("racist_data_set.csv")
create_new_frame()
new_data = pd.DataFrame(tweet_list,columns=['tweets'])
print(new_data.shape)
new_data.to_csv('biden_twitter_set.csv',index=True)