# Debot
Twitter bot detection using deep learning. This project is structured as following : 
## Running 
python -i App.py (interactive mode to play around with the data)

Disclaimer : Currently missing a LOT of files required for running (eg. datasets, database files, word2vec etc.)

## Requirements
* Tweepy
* Gensim
* NLTK
* Keras
* Tensorflow

## utils
This holds the utilities for the project. Mainly stores datasets and the scripts to extract them. Fetcher.py contains useful functions that is used by different <dataset>_reader.py's to read from the dataset and store only the users' info into a Sqlite3 database. From there, tweet_saver.py is run which downloads upto 1200 tweets per user. It has all sorts of error handling built in to avoid failure.
## keras
Placeholder
## models
Currently, 3 models are defined:
* Tweet
* User
* UserMaker
## vectorize
This contains the pre trained gLoVe model that is used to get word-vector representations (https://nlp.stanford.edu/projects/glove/). The gLoVe model was converted to a Word2Vec model (easier for processing) using Gensim. 

## Dataset
Since I had trouble finding suitable datasets for this project, here is whatever I've found : 

(Cresci 2017) - https://botometer.iuni.iu.edu/bot-repository/datasets.html

(ASONAM Honeypot 2015) - http://www.public.asu.edu/~fmorstat/bottutorial/ Many of the tweets in this dataset are in Arabic which is a bit disappointing. Also since it is older, a lot of the accounts have already been suspended.
