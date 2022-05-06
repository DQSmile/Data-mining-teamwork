import os
from project.utils.config import PROCESSED_DATA_DIR


def hydrating(date_str):
    tsv_filename = '{}.tsv'.format(date_str)
    input_filename = os.path.join(PROCESSED_DATA_DIR, 'tsv', tsv_filename)
    output_dir = os.path.join(PROCESSED_DATA_DIR, 'hydrated_tweets', date_str)
    command_line = f"python get_metadata.py -i {input_filename} -o {output_dir} -k api_keys.json"
    os.system(f'cmd /c {command_line}')


if __name__ == '__main__':
    date_str = '2020-03-22'
    hydrating(date_str)
