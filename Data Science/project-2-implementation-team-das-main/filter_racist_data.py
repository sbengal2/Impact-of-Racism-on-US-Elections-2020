import re
import pandas as pd
tweet_list = []
data = pd.read_csv("/Volumes/My Passport/MongoData/dataTwittercompletedataset.csv", lineterminator='\n',chunksize=1000,low_memory=False)
print('reading done')


def to_lower_case(tweet):
    return tweet.lower()

def filter_tweets(tweet):
    key_words = ["racism","#blacklivesmatter","george floyd","blacks","african american","#whatmatters2020","racist","white supremacy","skin tone","Supremacy",
                "supremacists","mexicans","superior","trump wall","intolerance","hate","Divide","Sadism","fascism","black","asians","migrants","immigrants","refugees","natives",
                 "american indians","black community","discrimination","discriminate","dicriminatory","structural racism","slaves","slavery","brown","muslims","black people","niggers","nigga","white boy",
                  "rosa parks","mandela","police brutality","brutality","latinos","negro","color","equality","breonna taylor","gandhi","kamala harris",
                  "obama","kanye west","dark","dark skin","hispanic","africans","elections2020","election day","#elections2020","afro","alligator","crow","brownie","brown skin",
                 "brown people","black skin","chinky","white trash","black trash","white power","indians","white-supremacy","ali baba","xeno","xenophobia","apu","black man","black woman",
                "blackie","blacky","hatred","racial disparities","black americans","anti-racism","black lives matter","bias","implicit bias","institutionalized racism","people of color"
                "oppression","black ethnicity","ethnic","ethnicity","racist policies","white privilege","blacklist"]
    patterns = [r'\b%s\b' % re.escape(word.strip()) for word in key_words]
    regex = re.compile('|'.join(patterns))
    if regex.search(to_lower_case(str(tweet))):
        return True
    return False

def create_new_frame(data_chunk):
    for index, row in data_chunk.iterrows():
        if filter_tweets(row['text']):
               tweet_list.append(row['text'])

count = 1
for chunk in data:
    create_new_frame(chunk)
    print(count)
    count += 1

new_data = pd.DataFrame(tweet_list, columns=['tweets'])
new_data.to_csv('racist_data.csv',index=False)