## Introduction
One of the primary applications of natural language processing is to automatically extract what topics people are discussing from large volumes of text. Some examples of large text could be feeds from social media, customer reviews of hotels, movies, etc, user feedbacks, news stories, e-mails of customer complaints etc.

Knowing what people are talking about and understanding their problems and opinions is highly valuable to businesses, administrators, political campaigns. And it’s really hard to manually read through such large volumes and compile the topics.

Thus is required an automated algorithm that can read through the text documents and automatically output the topics discussed.


## Topic modeling
![topicawareness](https://user-images.githubusercontent.com/62256302/86842392-bf116c80-c0c2-11ea-97ad-fbcdb204e69f.jpeg)

Topic modeling is a type of statistical modeling for discovering the abstract “topics” that occur in a collection of documents.

### Latent Dirichlet Allocation

Latent Dirichlet Allocation (LDA) is an example of topic model and is used to classify text in a document to a particular topic. 
It builds a topic per document model and words per topic model, modeled as Dirichlet distributions.


## What does LDA do?
LDA’s approach to topic modeling is it considers each document as a collection of topics in a certain proportion. And each topic as a collection of keywords, again, in a certain proportion.

Once you provide the algorithm with the number of topics, all it does it to rearrange the topics distribution within the documents and keywords distribution within the topics to obtain a good composition of topic-keywords distribution.

## When I say topic, what is it actually and how it is represented?

A topic is nothing but a collection of dominant keywords that are typical representatives. Just by looking at the keywords, you can identify what the topic is all about.

### Import Newsgroups Data
We will be using the 20-Newsgroups dataset for this exercise. This version of the dataset contains about 11k newsgroups posts from 20 different topics. This is available as newsgroups.json.

### Data Pre-processing

We will perform the following steps:
1. Tokenization: Split the text into sentences and the sentences into words. Lowercase the words and remove punctuation.
2. Words that have fewer than 3 characters are removed.
3. All stopwords are removed.
4. Words are lemmatized — words in third person are changed to first person and verbs in past and future tenses are changed into present.
5. Words are stemmed — words are reduced to their root form.

### Building the Topic Model
We have everything required to train the LDA model. In addition to the corpus and dictionary, you need to provide the number of topics as well.

Apart from that, alpha and eta are hyperparameters that affect sparsity of the topics. According to the Gensim docs, both defaults to 1.0/num_topics prior.

chunksize is the number of documents to be used in each training chunk. update_every determines how often the model parameters should be updated and passes is the total number of training passes.

 ### View the topics in LDA model
The above LDA model is built with 20 different topics where each topic is a combination of keywords and each keyword contributes a certain weightage to the topic.

You can see the keywords for each topic and the weightage(importance) of each keyword using lda_model.print_topics() as shown next.

### How to interpret this?

Topic 0 is a represented as _0.016“car” + 0.014“power” + 0.010“light” + 0.009“drive” + 0.007“mount” + 0.007“controller” + 0.007“cool” + 0.007“engine” + 0.007“back” + ‘0.006“turn”.

It means the top 10 keywords that contribute to this topic are: ‘car’, ‘power’, ‘light’.. and so on and the weight of ‘car’ on topic 0 is 0.016.

The weights reflect how important a keyword is to that topic.

## Important links:
<https://www.machinelearningplus.com/nlp/topic-modeling-gensim-python/>
<https://towardsdatascience.com/topic-modeling-and-latent-dirichlet-allocation-in-python-9bf156893c24>
