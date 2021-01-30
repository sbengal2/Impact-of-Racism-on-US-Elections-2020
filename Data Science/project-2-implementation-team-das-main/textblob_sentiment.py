from textblob import TextBlob
import pandas as pd
import numpy as np


def analyze_tweets():
    file_name = input("enter file name: ")
    path = file_name + ".csv"
    data = pd.read_csv(path)
    data['Subjectivity'] = data['tweets'].apply(get_text_subjectivity)
    data['Polarity'] = data['tweets'].apply(get_text_polarity)
    data['Analysis'] = data['Polarity'].apply(getAnalysis)
    data.to_csv(file_name + ".csv", index=False)


def analyze_comments():
    file_name = input("enter file name: ")
    path = file_name + ".csv"
    data = pd.read_csv(path)
    data['Subjectivity'] = data['comments'].apply(get_text_subjectivity)
    data['Polarity'] = data['comments'].apply(get_text_polarity)
    data['Analysis'] = data['Polarity'].apply(getAnalysis)
    data.to_csv(file_name + ".csv", index=False)


def get_text_subjectivity(tweet):
    return TextBlob(tweet).sentiment.subjectivity


def get_text_polarity(text):
    return TextBlob(text).sentiment.polarity


def getAnalysis(score):
    if score < 0:
        return 'Negative'
    elif score == 0:
        return 'Neutral'
    else:
        return 'Positive'


