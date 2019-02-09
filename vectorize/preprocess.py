from nltk.tokenize import TweetTokenizer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn, stopwords
from nltk import word_tokenize, pos_tag
from functools import lru_cache

wnl = WordNetLemmatizer()
lemmatize = lru_cache(maxsize=50000)(wnl.lemmatize)
tweet_tokenizer = TweetTokenizer()
stop_words = set(stopwords.words('english'))

def tokenize_filter(tweet):

    word_list = tweet_tokenizer.tokenize(tweet)
    new_list = []
    for token in word_list:
        if token.startswith("@"):
            new_list.append('mention')
        elif token.startswith("http") or token.startswith("www."):
            new_list.append('url')
        elif token.startswith('#'):
            new_list.append('hashtag')
        elif token not in stop_words:
            new_list.append(token.lower())
    return new_list

def lemmatize_filter(token_list):
    pos_tagged_tweet = pos_tag(token_list)
    new_list = []
    for word, tag in pos_tagged_tweet:
        wntag = tag[0].lower()
        wntag = wntag if wntag in ['a', 'r', 'n', 'v'] else None
        if not wntag:
            new_list.append(word)
        else:
            new_list.append(lemmatize(word, wntag))
    return new_list
