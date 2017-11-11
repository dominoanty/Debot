"""
Module for Tweet and any subsequent functions that the model might require

"""
import params
from vectorize.vectorize import model
from nltk.tokenize import TweetTokenizer

class Tweet:
    """ Model class for a Tweet. """

    def __init__(self, tweet, user):
        try:
            self.id = tweet["id"]
            self.text = tweet["text"]
            self.tokenized_text = None
            self.vector_form = None
            self.time = tweet["created_at"]
            if "retweeted_status" in tweet:
                self.is_rt = True
            else:
                self.is_rt = False
            self.user = user
        except ValueError as VE:
            return None
    
    def tokenize_tweet(self):
        pass
    
    def vectorize_tweet(self):
        pass
