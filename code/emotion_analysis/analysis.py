import os
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm

''' load csv file '''
file = pd.read_csv(r"data/with_sentiment.csv", on_bad_lines = 'warn')

print(file.columns)
print(file)
# file = file[file["tweet_retweet_count"].apply(pd.to_numeric, errors='coerce').notna()].dropna()
# print(file)

def linear_graph(attribute):
    fig = plt.figure()

    ax1 = fig.add_subplot(231)
    ax2 = fig.add_subplot(232)
    ax3 = fig.add_subplot(233)
    ax4 = fig.add_subplot(234)
    ax5 = fig.add_subplot(235)
    ax6 = fig.add_subplot(236)

    # drop tweets with less count
    row = file[attribute] > 100

    ax1.scatter(file[attribute][row], file["sadness"][row])
    ax1.title.set_text('sadness')
    ax2.scatter(file["joy"][row], file[attribute][row])
    ax2.title.set_text('joy')
    ax3.scatter(file["love"][row], file[attribute][row])
    ax3.title.set_text('love')
    ax4.scatter(file["anger"][row], file[attribute][row])
    ax4.title.set_text('anger')
    ax5.scatter(file["fear"][row], file[attribute][row])
    ax5.title.set_text('fear')
    ax6.scatter(file["surprise"][row], file[attribute][row])
    ax6.title.set_text('surprise')

    plt.show()

    fig.savefig(r'data/graph/' + "linear_graph_" + attribute + '.jpg')



''' linear_graph '''
linear_attributes = ['tweet_retweet_count', 'tweet_favorite_count', 'user_followers_count',\
                    'user_friends_count', 'user_listed_count', 'user_favourites_count',\
                    'user_statuses_count']

for attribute in linear_attributes:
    linear_graph(attribute)
