import json
import os
import random
from project.utils.config import PROCESSED_DATA_DIR

list_tweets = None


def filtering(date_str, keyword_lst=None):
    filename = f'{date_str}_short.json'
    json_file = os.path.join(PROCESSED_DATA_DIR, 'hydrated_tweets', filename)

    with open(json_file, "r") as myfile:
        list_tweets = list(myfile)

    filter_filename = os.path.join(PROCESSED_DATA_DIR, 'hydrated_tweets', f'{date_str}_filter.json')
    with open(filter_filename, "w") as filter_file:
        for i in list_tweets:
            i_item = json.loads(i)
            if 'mask' in i_item['text'].lower():
                filter_file.write(i)


if __name__ == '__main__':
    date_str = '2020-03-22'
    keyword_lst = ['mask']
    filtering(date_str=date_str, keyword_lst=keyword_lst)
