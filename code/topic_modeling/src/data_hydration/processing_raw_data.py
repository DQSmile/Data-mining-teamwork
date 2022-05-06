import os
import csv
import gzip
import shutil
import linecache
import numpy as np
import pandas as pd
import ipywidgets as widgets
from shutil import copyfile

from project.utils.config import RAW_DATA_DIR, PROCESSED_DATA_DIR


def unzip_daily_data(date_str):
    daily_dir = os.path.join(RAW_DATA_DIR, 'covid19_twitter', 'dailies', date_str)

    # Unzips the dataset and gets the TSV dataset
    gz_filename = '{}_clean-dataset.tsv.gz'.format(date_str)
    tsv_filename = '{}.tsv'.format(date_str)

    input_file = os.path.join(daily_dir, gz_filename)
    output_file = os.path.join(PROCESSED_DATA_DIR, 'tsv', tsv_filename)

    with gzip.open(input_file, 'rb') as f_in:
        with open(output_file, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

    # Deletes the compressed GZ file
    # os.unlink("clean-dataset.tsv.gz")

    # Gets all possible languages from the dataset
    df = pd.read_csv(output_file, sep="\t")
    # lang_list = df.lang.unique()
    # lang_list = sorted(np.append(lang_list, 'all'))
    # lang_picker = widgets.Dropdown(options=lang_list, value="all")
    # print(lang_picker)
    return df


if __name__ == '__main__':
    date_str = '2020-03-22'

    unzip_daily_data(date_str)
