import pandas as pd
from transformers import pipeline
from tqdm import tqdm

''' load csv file '''
file = pd.read_csv(r"data/all_tweets.csv", on_bad_lines = 'error')
file = file.iloc[:, 1:]
print(file.columns)
print(file)

file.drop_duplicates(subset=['full_text'], keep='first', inplace=True)
print(file)

''' load language detector model '''
# nlp = spacy.load('en_core_web_sm')
# Language.factory("language_detector", func=get_lang_detector)
# nlp.add_pipe('language_detector', last=True)

''' load sentiment analysis model '''
classifier = pipeline("text-classification",model='bhadresh-savani/distilbert-base-uncased-emotion', return_all_scores=True, device=0)

result = {"keywords":[], "tweet_id":[], "tweet_created_at":[], "full_text":[], "hashtags":[], "tweet_retweet_count":[], \
    "tweet_favorite_count":[], "user_id":[], "user_name":[], "user_location":[], \
    "user_created_at":[], "user_followers_count":[], "user_friends_count":[], "user_listed_count":[], \
    "user_favourites_count":[], "user_statuses_count":[], "sadness":[], \
    "joy":[], "love":[], "anger":[], "fear":[], "surprise":[]}

for row in tqdm(file.itertuples()):
    # print(doc._.language)
    if True:
        print(row[1],row[2],row[4])
        prediction = classifier(row[4])
        result["keywords"].append(row[1])
        result["tweet_id"].append(row[2])
        result["tweet_created_at"].append(row[3])
        result["full_text"].append(row[4])
        result["hashtags"].append(row[5])
        result["tweet_retweet_count"].append(row[6])
        result["tweet_favorite_count"].append(row[7])
        result["user_id"].append(row[8])
        result["user_name"].append(row[9])
        result["user_location"].append(row[10])
        result["user_created_at"].append(row[11])
        result["user_followers_count"].append(row[12])
        result["user_friends_count"].append(row[13])
        result["user_listed_count"].append(row[14])
        result["user_favourites_count"].append(row[15])
        result["user_statuses_count"].append(row[16])
        result["sadness"].append(prediction[0][0]["score"])
        result["joy"].append(prediction[0][1]["score"])
        result["love"].append(prediction[0][2]["score"])
        result["anger"].append(prediction[0][3]["score"])
        result["fear"].append(prediction[0][4]["score"])
        result["surprise"].append(prediction[0][5]["score"])

result = pd.DataFrame(result)
print(result)
result.to_csv(r"data/with_sentiment.csv",index=False)
