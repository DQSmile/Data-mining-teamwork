import os
from project.utils.config import PROCESSED_DATA_DIR

num_samples = 1000


def parsing_sample(date_str):
    filename = f'{date_str}_sample_{str(num_samples)}.json'
    json_file = os.path.join(PROCESSED_DATA_DIR, 'hydrated_tweets', filename)
    command_line = f"python parse_json_lite.py {json_file} p"
    os.system(f'cmd /c {command_line}')


if __name__ == '__main__':
    date_str = '2020-03-22'
    parsing_sample(date_str)
