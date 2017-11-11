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
Currently, 2 models are defined:
### Tweet
### User
## vectorize
This contains the pre trained gLoVe model that is used to get word-vector representations (https://nlp.stanford.edu/projects/glove/). The gLoVe model was converted to a Word2Vec model (easier for processing) using Gensim. 
