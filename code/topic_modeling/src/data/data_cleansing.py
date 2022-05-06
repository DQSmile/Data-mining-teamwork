COL = 'tweet_retweet_count'
import re
import numpy as np
import pandas as pd

from utils.logger import logger
from utils.data_porter import read_from_csv
from utils.config import PROCESSED_DATA_DIR

desired_width = 320
pd.set_option('display.width', desired_width)
# pd.set_option('display.max_columns', 10)
pd.set_option('display.max_columns', None)


def data_loading():
    logger.info('Start Data Loading...')
    file_lst = [(1, 49), (50, 100), (101, 200), (201, 300), (301, 400), (401, 500)]

    # Get the file name needed to be loaded
    selected_file = []
    for file_start, file_end in file_lst:
        selected_file.append('output_day{}-{}.csv'.format(str(file_start), str(file_end)))
    logger.info('Selected File Name: {}'.format('/'.join(selected_file)))

    raw_data_lst = []
    for file in selected_file:
        tmp_data = read_from_csv(file, PROCESSED_DATA_DIR, index_col=0)
        raw_data_lst.append(tmp_data)

    raw_data = pd.concat(raw_data_lst)

    print(raw_data)

    desc = raw_data.describe().T
    desc['count'] = desc['count'].astype(int)
    print(desc)
    logger.debug(f'Sample Number:{len(raw_data)}')
    return raw_data


def data_cleansing(data):
    data = data[data.tweet_retweet_count.apply(lambda x: isinstance(x, int))]
    print(data)
    print(len(data))


if __name__ == '__main__':
    raw_data = data_loading()
    data = data_cleansing(raw_data)
