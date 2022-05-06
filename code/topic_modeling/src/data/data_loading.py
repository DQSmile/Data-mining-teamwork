import pandas as pd

from utils.logger import logger
from utils.data_porter import read_from_csv
from utils.config import PROCESSED_DATA_DIR


def data_loading(date_from, date_to, filter=None, has_content=None, matrix=None, exclusive=True):
    logger.info('Start Data Loading...')
    file_lst = [(1, 49), (50, 100), (101, 200), (201, 300), (301, 400), (401, 500)]

    # Get the file name needed to be loaded
    selected_file = []
    for file_start, file_end in file_lst:
        if file_start < date_to and file_end > date_from:
            selected_file.append('output_day{}-{}.csv'.format(str(file_start), str(file_end)))
    logger.info('Load Date from Day {} to Day {}.'.format(str(date_from), str(date_to)))
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

    if filter:
        logger.debug(f'Sample Number Before filter:{len(raw_data)}')
        raw_data = raw_data[raw_data['keywords'].apply(lambda x: filter not in x)]
        logger.debug(f'Sample Number After filter:{len(raw_data)}')
    logger.info('Data Loading Complete!')

    if has_content:
        logger.debug(f'Sample Number Before has_content:{len(raw_data)}')
        raw_data = raw_data[raw_data['keywords'].apply(lambda x: has_content in x)]
        logger.debug(f'Sample Number After has_content:{len(raw_data)}')

    # if exclusive:
    #     logger.debug(f'Sample Number Before Exclusive Check:{len(raw_data)}')
    #     raw_data['keywords_num'] = raw_data['keywords'].apply(lambda x: len(eval(x)))
    #     raw_data = raw_data[raw_data['keywords_num'] == 1]
    #     logger.debug(f'Sample Number After Exclusive Check:{len(raw_data)}')

    if not matrix:
        return raw_data
    elif matrix == 'tweet_retweet_count':
        influential_df = raw_data[raw_data['tweet_retweet_count'] >= 4]
        noninfluential_df = raw_data[raw_data['tweet_retweet_count'] < 4]
        logger.info(
            f'Using matrix {matrix}: influential({len(influential_df)}) vs non-influential({len(noninfluential_df)})')
        return influential_df, noninfluential_df
    elif matrix == 'user_followers_count':
        influential_df = raw_data[raw_data['user_followers_count'] >= 1000]
        noninfluential_df = raw_data[raw_data['user_followers_count'] < 1000]
        noninfluential_df = raw_data[raw_data['user_followers_count'] < 1000]
        logger.info(
            f'Using matrix {matrix}: influential({len(influential_df)}) vs non-influential({len(noninfluential_df)})')
        return influential_df, noninfluential_df
