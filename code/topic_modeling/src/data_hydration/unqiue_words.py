import os
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from project.utils.config import PROCESSED_DATA_DIR

num_samples = 1000
no_top_unique_words = "20"  # @param {type:"string"}


def unique(date_str):
    filename = f'{date_str}_sample_{str(num_samples)}.tsv'
    tsv_file = os.path.join(PROCESSED_DATA_DIR, 'hydrated_tweets', filename)
    df = pd.read_csv(tsv_file, sep="\t")

    result = Counter(" ".join(df['text'].values.tolist()).split(" ")).items()
    df2 = pd.DataFrame(result)
    df2.columns = ['Word', 'Frequency']
    df2 = df2[df2.Word != ""]  # Deletes the empty spaces counted
    df2 = df2.sort_values(['Frequency'], ascending=[False])  # Sort dataframe by frequency (Descending)

    print('\033[1mTop ' + no_top_unique_words + ' most unique words used from the dataset\033[0m \n')
    print(df2.head(int(no_top_unique_words)).to_string(index=False))  # Prints the top N unique words used
    print("\n")
    df3 = df2.head(int(no_top_unique_words))
    df3.plot(y='Frequency', kind='pie', labels=df3['Word'], figsize=(9, 9), autopct='%1.1f%%',
             title='Top ' + no_top_unique_words + ' most unique words used from the dataset')
    plt.show()  # This command tells the system to draw the plot in Pycharm.


if __name__ == '__main__':
    date_str = '2020-03-22'
    unique(date_str)
