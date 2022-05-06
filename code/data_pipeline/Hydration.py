from twarc import Twarc
import pandas as pd

# Twitter Developer Account Credentials
consumer_key="3cZsDxk9VYcNUchrdCMoWOrUp"
consumer_secret="Fq0qZGl5ZN7hCZZn4VQU0oCi5a4Mqhmpk0b5NPmyApPX6ogzWL"
bearer_token = "AAAAAAAAAAAAAAAAAAAAAJPxUgEAAAAAi%2B4nqFC58NIz9j5%2FyXcK7FACEw8%3Dehp5LJcabsLjYHDSOmo6VoOpr6T0axhlsriZRXKaTqLukSsZeB"
access_token="1449206167352143872-77kY35YZri9j4KhTBBicQMmMapaQAi"
access_token_secret="d0buu2ZsJNNlggB39bG4GDx9yOr1aFJKDQznEKWk1m7XU"
t = Twarc(consumer_key, consumer_secret, access_token, access_token_secret)

## Function to identify topic keyword:
keywords = ['mask','n95','n-95','face shield','faceshield','wash hand','washhand','washurhands','washyourhands',
'handsanitizer','safe distance','safe distancing','socialdistancing','socially distance','selfisolating','stayhome','stayhomestaysafe',
'work from home','workfromhome','workingfromhome','wfh','home school','homeschool','hygiene','sanitary','protection',
'vaccine','vaccinated','quarantine']
def topic(text):
    set = []
    for word in keywords:
        if word in text.lower():
            set.append(word)
    return set

## Function to store hashtag:
def hashtag(input):
    if input:
        return input[0]['text']
    else:
        return input

# CSV prefix & suffix
csv_perfix = 'corona_tweets_401-500/corona_tweets_'
#csv_perfix = 'corona_tweets_'
csv_suffix = '.csv'

output = []
for i in range(401,501):
    csv = csv_perfix+str(i)+csv_suffix
    df = pd.read_csv(csv, header=None)
    df = df.sample(frac=0.01,random_state=1)
    df_id = df[0]
    tweets = []
    for tweet in t.hydrate(df_id):
        if topic(tweet['full_text']):
            tweets.append([
                # Keyword
                topic(tweet['full_text']),
                # Tweet Info
                tweet['id'], tweet['created_at'], tweet['full_text'], hashtag(tweet['entities']['hashtags']), 
                tweet['retweet_count'], tweet['favorite_count'],  
                # User Info
                tweet['user']['id'],tweet['user']['name'],tweet['user']['location'],tweet['user']['created_at'],tweet['user']['followers_count'],
                tweet['user']['friends_count'],tweet['user']['listed_count'],tweet['user']['favourites_count'],tweet['user']['statuses_count']
            ])
    tweets_df = pd.DataFrame(tweets, columns=['keywords',
            # tweet
            'tweet_id', 'tweet_created_at', 'full_text','hashtags', 
            'tweet_retweet_count', 'tweet_favorite_count', 
            # user
            'user_id','user_name','user_location','user_created_at','user_followers_count',
            'user_friends_count','user_listed_count','user_favourites_count','user_statuses_count'])
    output.append(tweets_df)

output_df = pd.concat(output)
output_df.to_csv('output6.csv',header=True, index=True)