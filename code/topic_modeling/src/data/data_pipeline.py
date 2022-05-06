import pandas as pd
from utils.logger import logger
from utils.data_porter import read_from_csv, save_to_csv
from utils.config import PROCESSED_DATA_DIR
from src.data.data_processing import data_cleaning, preprocess_data

desired_width = 320
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns', 20)


def data_loading_full():
    logger.info('Start Loading Full Data Set ...')
    file_lst = [(1, 49), (50, 100), (101, 200), (201, 300), (301, 400), (401, 500)]

    # Get the file name needed to be loaded
    selected_file = []
    for file_start, file_end in file_lst:
        selected_file.append('output_day{}-{}.csv'.format(str(file_start), str(file_end)))
        logger.info('Load Date from Day {} to Day {}.'.format(str(file_start), str(file_end)))
    logger.info('Selected File Name: {}'.format('/'.join(selected_file)))

    raw_data_lst = []
    for file in selected_file:
        tmp_data = read_from_csv(file, PROCESSED_DATA_DIR, index_col=0)
        raw_data_lst.append(tmp_data)

    raw_data = pd.concat(raw_data_lst)
    raw_data.drop(columns=['0'], inplace=True)
    print(raw_data)

    desc = raw_data.describe().T
    desc['count'] = desc['count'].astype(int)
    print(desc)
    logger.debug(f'Sample Number:{len(raw_data)}')

    return raw_data


if __name__ == '__main__':
    # raw_data = data_loading_full()
    # save_to_csv(raw_data, 'output_full.csv', PROCESSED_DATA_DIR)

    raw_data = read_from_csv('output_full.csv', PROCESSED_DATA_DIR)

    # Data preprocessing
    data = data_cleaning(raw_data)
    print(data)
    save_to_csv(data, 'output_full_clean.csv', PROCESSED_DATA_DIR)

    # data = preprocess_data(data)
    # print(data)
    # save_to_csv(data, 'output_full_noun.csv', PROCESSED_DATA_DIR)
