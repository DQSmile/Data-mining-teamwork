import os
import pickle
import gensim
import pyLDAvis
import pyLDAvis.gensim_models
import pandas as pd
import gensim.corpora as corpora
import matplotlib.pyplot as plt
from pprint import pprint
from wordcloud import WordCloud
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel

from utils.logger import logger
from utils.config import RESULT_DIR, MODEL_DIR
from src.data.data_loading import data_loading
from src.data.data_processing import data_cleaning, preprocess_data, STOPWORDS_FULL
from src.lda.optimal_topics_num import compute_coherence_values, show_coherence, select_optimal_model

# number of topics
TOPICS_NUM = 10

desired_width = 320
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns', 10)


def exploratory_analysis(data_df):
    logger.info('Start Data Exploratory Analysis...')
    # Join the different processed titles together.
    long_string = ','.join(list(data_df['full_text_processed'].values))
    # Create a WordCloud object
    wordcloud = WordCloud(stopwords=STOPWORDS_FULL, background_color="white", max_words=5000, contour_width=3,
                          contour_color='steelblue')
    # Generate a word cloud
    wordcloud.generate(long_string)
    # Visualize the word cloud
    wordcloud.to_image()

    # Display the generated image:
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()
    logger.info('Data Exploratory Analysis Complete!')


def data_prepare(data_df):
    def sent_to_words(sentences):
        for sentence in sentences:
            # deacc=True removes punctuations
            yield (gensim.utils.simple_preprocess(str(sentence), deacc=True))

    def remove_stopwords(texts):
        return [[word for word in simple_preprocess(str(doc))
                 if word not in STOPWORDS_FULL] for doc in texts]

    logger.info('Start Data Preparation...')
    data = data_df.full_text_processed.values.tolist()
    data_words = list(sent_to_words(data))
    # remove stop words
    data_words = remove_stopwords(data_words)
    print(data_words[:1][0][:30])

    # Create Dictionary
    id2word = corpora.Dictionary(data_words)
    # Create Corpus
    texts = data_words
    # Term Document Frequency
    corpus = [id2word.doc2bow(text) for text in texts]
    # View
    print(corpus[:1][0][:30])

    logger.info('Data Preparation Complete!')

    return corpus, id2word, data_words


def training(corpus, id2word):
    logger.info('Start LDA model Training...')
    # Build LDA model
    lda_model = gensim.models.LdaMulticore(corpus=corpus,
                                           id2word=id2word,
                                           num_topics=TOPICS_NUM)
    # Print the Keyword in the 10 topics
    pprint(lda_model.print_topics())
    doc_lda = lda_model[corpus]
    logger.info('LDA model Training Complete!')
    logger.info('LDA model Training Complete!')
    return lda_model


def coherence(model, id2word, text):
    # Compute Coherence Score
    coherence_model_lda = CoherenceModel(model=model, texts=text, dictionary=id2word, coherence='c_v')
    coherence_lda = coherence_model_lda.get_coherence()
    print('\nCoherence Score: ', coherence_lda)


def training_mallet(corpus, id2word, data):
    mallet_path = 'D:\\OneDrive\\Programming\\documents_python\\NUS_Courses\\CS5344\\Course-CS5344\\project\\mallet-2.0.8'
    ldamallet = gensim.models.wrappers.LdaMallet(mallet_path, corpus=corpus, num_topics=20, id2word=id2word)
    pprint(ldamallet.show_topics(formatted=False))
    # Compute Coherence Score
    coherence_model_ldamallet = CoherenceModel(model=ldamallet, texts=data, dictionary=id2word,
                                               coherence='c_v')
    coherence_ldamallet = coherence_model_ldamallet.get_coherence()
    print('\nCoherence Score: ', coherence_ldamallet)


def analyzing(lda_model, corpus, id2word, label):
    logger.info('Start LDA model Analyzing...')
    # Visualize the topics
    # pyLDAvis.enable_notebook()
    LDAvis_data_filepath = os.path.join(MODEL_DIR, 'ldavis_prepared_{}_{}'.format(
        label, str(TOPICS_NUM)))
    # # this is a bit time consuming - make the if statement True
    # # if you want to execute visualization prep yourself
    if 1 == 1:
        LDAvis_prepared = pyLDAvis.gensim_models.prepare(lda_model, corpus, id2word)
        with open(LDAvis_data_filepath, 'wb') as f:
            pickle.dump(LDAvis_prepared, f)
    # load the pre-prepared pyLDAvis data from disk
    with open(LDAvis_data_filepath, 'rb') as f:
        LDAvis_prepared = pickle.load(f)

    html_name = 'ldavis_prepared_{}_{}.html'.format(label, str(TOPICS_NUM))
    html_path = os.path.join(RESULT_DIR, html_name)
    pyLDAvis.save_html(LDAvis_prepared, html_path)
    logger.info('Visualization html is ready.')
    logger.info('LDA model Analyzing Complete!')


def lda_pipeline(raw_data, label):
    logger.info(f'----------Start LDA pipeline for label: {label}')
    # Data preprocessing
    data = data_cleaning(raw_data)
    data = preprocess_data(data)

    # EDA
    exploratory_analysis(data)

    # LDA
    corpus, id2word, data_words = data_prepare(data)
    # lda_model = training(corpus, id2word)

    # mallet_model = training_mallet(corpus, id2word, data)

    # coherence(model=lda_model, id2word=id2word, text=data_words)
    limit = 5
    start = 2
    step = 1

    model_list, coherence_values = compute_coherence_values(
        dictionary=id2word, corpus=corpus, texts=data_words,
        limit=limit, start=start, step=step)

    show_coherence(coherence_values,
                   limit=limit, start=start, step=step)
    model = select_optimal_model(model_list, coherence_values, start=start, step=step)

    analyzing(model, corpus, id2word, label=label)


if __name__ == '__main__':
    # date_range_lst = [(1, 49), (50, 100), (101, 200), (201, 300), (301, 400), (401, 500)]
    # matrix_lst = ['tweet_retweet_count', 'user_followers_count']
    date_range_lst = [(301, 400)]
    matrix_lst = ['user_followers_count']
    for date_from, date_to in date_range_lst:
        for matrix in matrix_lst:
            logger.info('From Day {} to Day {} for {}'.format(
                str(date_from), str(date_to), matrix).center(20, '='))
            influential_df, non_influential_df = data_loading(
                date_from=date_from,
                date_to=date_to,
                matrix=matrix)
            lda_pipeline(
                raw_data=influential_df,
                label='{}_{}_{}_influential'.format(matrix, str(date_from), str(date_to)))
            # lda_pipeline(
            #     raw_data=non_influential_df,
            #     label='{}_{}_{}_non_influential'.format(matrix, str(date_from), str(date_to)))
