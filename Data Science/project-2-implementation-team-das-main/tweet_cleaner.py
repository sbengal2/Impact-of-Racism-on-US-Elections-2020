import re
import numpy as np
import pandas as pd


def remove_pattern(text, pattern):
    r = re.findall(pattern, text)
    for i in r:
        text = re.sub(i, '', text)
    return text


def clean_tweets(tweets):
    tweets = np.vectorize(remove_pattern)(tweets, "RT @[\w]*:")
    tweets = np.vectorize(remove_pattern)(tweets, "@[\w]*")
    tweets = np.vectorize(remove_pattern)(tweets, "https?://[A-Za-z0-9./]*")
    tweets = np.core.defchararray.replace(tweets, "[^a-zA-Z]", " ")
    return tweets


def clean_it():
    file_name = input("enter file name: ")
    path = file_name + ".csv"
    data = pd.read_csv(path)
    data['tweets'] = clean_tweets(data['tweets'])
    output = input("enter ouput file name: ")
    data.to_csv(output+".csv",index=False)


clean_it()