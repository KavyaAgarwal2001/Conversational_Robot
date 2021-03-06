# -*- coding: utf-8 -*-
"""TopicModellingUsingNLTK&Gensim.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1icVgcf93ZlYJcZkPycd7W8IewrsbKf4x
"""

#Reference 1 : https://towardsdatascience.com/topic-modelling-in-python-with-nltk-and-gensim-4ef03213cd21
#Reference 2 : https://www.machinelearningplus.com/nlp/topic-modeling-gensim-python/

"""**Topic Modelling**--

Topic Modeling is a technique to extract the hidden topics from large volumes of text.

Latent Dirichlet Allocation (LDA): a widely used topic modelling technique. 
Have applied LDA to convert set of research papers to a set of topics.

Research paper topic modelling is an unsupervised machine learning method that helps us discover hidden semantic structures in a paper, that allows us to learn topic representations of papers in a corpus. The model can be applied to any kinds of labels on documents, such as tags on posts on the website.
"""

#research paper text data is just a bunch of unlabeled texts
!wget https://github.com/susanli2016/Machine-Learning-with-Python/blob/master/dataset.csv

"""**Text Cleaning**"""

#function to clean our texts and return a list of tokens:

import spacy
spacy.load('en')
from spacy.lang.en import English
parser = English()

def tokenize(text):
    lda_tokens = []
    tokens = parser(text)
    for token in tokens:
        if token.orth_.isspace():
            continue
        elif token.like_url:
            lda_tokens.append('URL')
        elif token.orth_.startswith('@'):
            lda_tokens.append('SCREEN_NAME')
        else:
            lda_tokens.append(token.lower_)
    return lda_tokens

#use NLTK’s Wordnet to find the meanings of words, synonyms, antonyms, and more.
#n addition, we use WordNetLemmatizer to get the root word.

import nltk
nltk.download('wordnet')

from nltk.corpus import wordnet as wn
def get_lemma(word):
    lemma = wn.morphy(word)
    if lemma is None:
        return word
    else:
        return lemma
    
from nltk.stem.wordnet import WordNetLemmatizer
def get_lemma2(word):
    return WordNetLemmatizer().lemmatize(word)

for w in ['dogs', 'ran', 'discouraged']:
    print(w, get_lemma(w), get_lemma2(w))

#Filter out stop words:

nltk.download('stopwords')
en_stop = set(nltk.corpus.stopwords.words('english'))

#Now we can define a function to prepare the text for topic modelling:

def prepare_text_for_lda(text):
    tokens = tokenize(text)
    tokens = [token for token in tokens if len(token) > 4]
    tokens = [token for token in tokens if token not in en_stop]
    tokens = [get_lemma(token) for token in tokens]
    return tokens

#Open up our data, read line by line, for each line, prepare text for LDA, then add to a list.
#Now we can see how our text data are converted:

import random
text_data = []
with open('dataset.csv') as f:
    for line in f:
        tokens = prepare_text_for_lda(line)
        if random.random() > .99:
            print(tokens)
            text_data.append(tokens)

"""**LDA with Gensim**"""

#First, we are creating a dictionary from the data,
#then convert to bag-of-words corpus and save the dictionary and corpus for future use.

from gensim import corpora
dictionary = corpora.Dictionary(text_data)

corpus = [dictionary.doc2bow(text) for text in text_data]

import pickle
pickle.dump(corpus, open('corpus.pkl', 'wb'))
dictionary.save('dictionary.gensim')

#We are asking LDA to find 5 topics in the data:

import gensim
NUM_TOPICS = 5
ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics = NUM_TOPICS, id2word=dictionary, passes=15)
ldamodel.save('model5.gensim')

topics = ldamodel.print_topics(num_words=4)
for topic in topics:
    print(topic)

#Let’s try a new document:

new_doc = 'Practical Bayesian Optimization of Machine Learning Algorithms'
new_doc = prepare_text_for_lda(new_doc)
new_doc_bow = dictionary.doc2bow(new_doc)
print(new_doc_bow)
print(ldamodel.get_document_topics(new_doc_bow))

ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics = 3, id2word=dictionary, passes=15)
ldamodel.save('model3.gensim')
topics = ldamodel.print_topics(num_words=4)
for topic in topics:
    print(topic)

#We can also find 10 topics:

ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics = 10, id2word=dictionary, passes=15)
ldamodel.save('model10.gensim')
topics = ldamodel.print_topics(num_words=4)
for topic in topics:
    print(topic)

"""**pyLDAvis**"""

!pip install pyLDAvis

#interpret the topics in a topic model that has been fit to a corpus of text data.

#Visualizing 5 topics:

dictionary = gensim.corpora.Dictionary.load('dictionary.gensim')
corpus = pickle.load(open('corpus.pkl', 'rb'))
lda = gensim.models.ldamodel.LdaModel.load('model5.gensim')
import pyLDAvis.gensim
lda_display = pyLDAvis.gensim.prepare(lda, corpus, dictionary, sort_topics=False)
pyLDAvis.display(lda_display)

#Visualizing 3 topics:

lda3 = gensim.models.ldamodel.LdaModel.load('model3.gensim')
lda_display3 = pyLDAvis.gensim.prepare(lda3, corpus, dictionary, sort_topics=False)
pyLDAvis.display(lda_display3)

#Visualizing 10 topics:

lda10 = gensim.models.ldamodel.LdaModel.load('model10.gensim')
lda_display10 = pyLDAvis.gensim.prepare(lda10, corpus, dictionary, sort_topics=False)
pyLDAvis.display(lda_display10)