import os
import random
from project.utils.config import PROCESSED_DATA_DIR

num_samples = 1000
list_tweets = None


def sampling(date_str, num_samples):
    filename = f'{date_str}_short.json'
    json_file = os.path.join(PROCESSED_DATA_DIR, 'hydrated_tweets', filename)

    with open(json_file, "r") as myfile:
        list_tweets = list(myfile)

    num_samples = len(list_tweets) if num_samples > len(list_tweets) else num_samples

    sample = random.sample(list_tweets, num_samples)

    sample_filename = os.path.join(PROCESSED_DATA_DIR, 'hydrated_tweets', f'{date_str}_sample_{str(num_samples)}.json')
    with open(sample_filename, "w") as sample_file:
        for i in sample:
            sample_file.write(i)


if __name__ == '__main__':
    date_str = '2020-03-22'
    sampling(date_str=date_str, num_samples=num_samples)
