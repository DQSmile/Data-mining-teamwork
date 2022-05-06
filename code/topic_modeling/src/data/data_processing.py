import re
import string
import pandas as pd
import preprocessor as p
from bs4 import BeautifulSoup
from wordcloud import STOPWORDS
from utils.logger import logger

import nltk
# nltk.download
# nltk.download('wordnet')
# nltk.download('stopwords')
# nltk.download('averaged_perceptron_tagger')
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer

STOPWORDS_SPEC = ["https", "rt", "covid19", "covid", "tco"]
STOPWORDS_FULL = set(STOPWORDS)
STOPWORDS_FULL.update(stopwords.words('english'))
STOPWORDS_FULL.update(STOPWORDS_SPEC)


def data_cleaning(raw_data):
    # to remove HTML tag
    def html_remover(data):
        beauti = BeautifulSoup(data, 'html.parser')
        return beauti.get_text()

    # to remove URL
    def url_remover(data):
        return re.sub(r'https\S', '', data)

    def web_associated(data):
        text = html_remover(data)
        text = url_remover(text)
        return text

    def remove_round_brackets(data):
        return re.sub('\(.*?\)', '', data)

    def remove_punc(data):
        trans = str.maketrans('', '', string.punctuation)
        return data.translate(trans)

    def white_space(data):
        return ' '.join(data.split())

    def complete_noise(data):
        new_data = remove_round_brackets(data)
        new_data = remove_punc(new_data)
        new_data = white_space(new_data)
        return new_data

    def remove_stopwords(data):
        tokens = data.split()
        tokens = [token for token in tokens if token not in STOPWORDS_FULL]
        return ' '.join(tokens)

    logger.info('Start Data Cleaning...')

    # Remove punctuation
    logger.info('Remove punctuation')
    raw_data['full_text_processed'] = raw_data['full_text'].map(lambda x: re.sub('[,\.!?]', '', x))
    # Convert the titles to lowercase
    logger.info('Convert the titles to lowercase')
    raw_data['full_text_processed'] = raw_data['full_text_processed'].map(lambda x: x.lower())
    # URLs, Mentions, etc.
    logger.info('URLs, Mentions, etc.')
    raw_data['full_text_processed'] = raw_data['full_text_processed'].map(lambda x: p.clean(x))
    # Removing the HTML tag and URL
    logger.info('Removing the HTML tag and URL')
    raw_data['full_text_processed'] = raw_data['full_text_processed'].map(lambda x: web_associated(x))
    # Some noise in the form of punctuations and white spaces, and text data under the parenthesis
    logger.info('Some noise in the form')
    raw_data['full_text_processed'] = raw_data['full_text_processed'].map(lambda x: complete_noise(x))
    # Remove Stopwords
    logger.info('Remove Stopwords')
    raw_data['full_text_processed'] = raw_data['full_text_processed'].map(lambda x: remove_stopwords(x))
    # Drop row with nan
    logger.info('Drop row with nan')
    raw_data.dropna(subset=["full_text_processed"], inplace=True)

    # Print out the first rows of papers
    print(raw_data['full_text_processed'].head())
    logger.info('Data Loading Cleaning Complete!')
    return raw_data


def preprocess_data(data_df):
    data = data_df['full_text_processed']
    lemmatizer = nltk.stem.WordNetLemmatizer()
    w_tokenizer = TweetTokenizer()

    def lemmatize_text(text):
        words = [(lemmatizer.lemmatize(w)) for w in w_tokenizer.tokenize((text))]
        return ' '.join(words)

    def keep_noun(text):
        tokens = nltk.word_tokenize(text)
        tags = nltk.pos_tag(tokens)
        nouns = [word for word, pos in tags if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS')]
        text = ' '.join(nouns)
        return text

    def to_str(words):
        return

    logger.info('Start Part-of-speech analysis: only noun remains...')
    data = data.apply(keep_noun)

    # logger.info('Start Lemmatize...')
    # data = data.apply(lemmatize_text)

    data_df['full_text_processed'] = pd.DataFrame(data)
    return data_df
