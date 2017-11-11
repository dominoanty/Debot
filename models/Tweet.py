"""
Module for Tweet and any subsequent functions that the model might require

"""
import params
from vectorize.vectorize import model
from nltk.tokenize import TweetTokenizer
from models.ArabicError import ArabicError

tweet_tokenizer = TweetTokenizer()

class Tweet:
    """ Model class for a Tweet. """

    def __init__(self, tweet, user):
        try:
            self.id = tweet["id"]
            self.text = tweet["text"]

            if params.ARABIC_TESTER.search(self.text) is not None:
                raise ArabicError("Text contains arabic!")

            self.tokenized_text = None
            self.vector_form = None
            self.time = tweet["created_at"]
            self.user = user

            if "retweeted_status" in tweet:
                self.is_rt = True
            else:
                self.is_rt = False

        except ValueError as VE:
            return None
    
    def tokenize_tweet(self):
        self.tokenized_text = tweet_tokenizer.tokenize(self.text)

    def vectorize_tweet(self):
        pass
