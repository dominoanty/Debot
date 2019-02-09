"""User module containing User Model and UserType Enum """
from enum import Enum
from .Tweet import Tweet
from .ArabicError import ArabicError

from vectorize.vectorize import model, BLANK_VECTOR, vectorize_filter
from vectorize.preprocess import tokenize_filter, lemmatize_filter
import pickle


class UserType(Enum):
    """The type of the user. Currently Human -> 0 and Bot -> 1"""
    HUMAN = 0
    BOT = 1

class UserData:

    def __init__(self, id, user_type, num_tweets):
        self.id = id
        self.user_type = user_type
        self.num_tweets = num_tweets


class User:
    """Model class that holds the information for a user."""

    def __init__(self, id, user_type):
        self.id = id
        self.tweets = []
        self.user_type = user_type
        self.followers = []
        self.followers_count = None
        self.following_count = None
        self.verified_status = None

    @staticmethod
    def create_user_uk(id, tweet_list):
        U = User(id, 2)
        U.tweets = [Tweet(tweet, U) for tweet in tweet_list]
        U.followers_count = tweet_list[0]['user']['followers_count']
        U.following_count = tweet_list[0]['user']['friends_count']
        U.verified_status = tweet_list[0]['user']['verified']
        for tweet in U.tweets:
            tweet.vector_form =  vectorize_filter(
                                    lemmatize_filter(
                                        tokenize_filter(tweet.text)))
        return U




    @staticmethod
    def create_user(filename, tweet_list, user_type, id=None):
        id = filename.split('\\')[-1].split('.')[0]
        U = User(id, user_type)
        try:
            U.tweets = [Tweet(tweet, U) for tweet in tweet_list]
            U.followers_count = tweet_list[0]['user']['followers_count']
            U.following_count = tweet_list[0]['user']['friends_count']
            U.verified_status = tweet_list[0]['user']['verified']

            for tweet in U.tweets:
                tweet.vector_form =  vectorize_filter(
                                        lemmatize_filter(
                                            tokenize_filter(tweet.text)))

            with open("data\\processed_data\\" + U.id + ".dat", "wb") as file:
                pickle.dump(U, file)
            
            return UserData(id, user_type, len(U.tweets))
            

        except ArabicError as A:
            return None
        except KeyError as K:
            print(K)
            return None
        return U

