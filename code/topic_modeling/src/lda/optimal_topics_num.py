import gensim
import matplotlib.pyplot as plt
from gensim.models import CoherenceModel

from utils.logger import logger
from pprint import pprint


def compute_coherence_values(dictionary, corpus, texts, limit=6, start=2, step=1):
    """
    Compute c_v coherence for various number of topics

    Parameters:
    ----------
    dictionary : Gensim dictionary
    corpus : Gensim corpus
    texts : List of input texts
    limit : Max num of topics

    Returns:
    -------
    model_list : List of LDA topic models
    coherence_values : Coherence values corresponding to the LDA model with respective number of topics
    """
    logger.info('Start Sequence LDA model Training to find optimal topics number...')
    coherence_values = []
    model_list = []
    for num_topics in range(start, limit, step):
        logger.info(f'Start Training Model with {num_topics} Topics')
        model = gensim.models.LdaMulticore(corpus=corpus,
                                           id2word=dictionary,
                                           num_topics=num_topics)
        model_list.append(model)
        coherencemodel = CoherenceModel(model=model, texts=texts, dictionary=dictionary, coherence='c_v')
        coherence_values.append(coherencemodel.get_coherence())

    return model_list, coherence_values


def show_coherence(coherence_values, limit=6, start=2, step=1):
    # Show graph
    x = range(start, limit, step)
    plt.plot(x, coherence_values)
    plt.xlabel("Num Topics")
    plt.ylabel("Coherence score")
    plt.legend("coherence_values", loc='best')
    plt.show()

    # Print the coherence scores
    for m, cv in zip(x, coherence_values):
        print("Num Topics =", m, " has Coherence Value of", round(cv, 4))


def select_optimal_model(model_list, coherence_values, start=2, step=1):
    best_model, best_coherence, num_topic, best_topic = None, 0, start, start
    for model, coh in zip(model_list, coherence_values):
        if coh > best_coherence:
            best_model, best_coherence = model, coh
            best_topic = num_topic
        num_topic += step
    logger.info(f'The Best Topic Number is: {best_topic}')
    # Select the model and print the topics
    model_topics = best_model.show_topics(formatted=False)
    pprint(best_model.print_topics(num_words=10))
    return best_model
