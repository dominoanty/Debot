"""User module containing User Model and UserType Enum """
from enum import Enum
from models.Tweet import Tweet 


class UserType(Enum):
    """The type of the user. Currently Human -> 0 and Bot -> 1"""


    HUMAN = 0
    BOT = 1

class User:
    """Model class that holds the information for a user."""

    def __init__(self, id, user_type):
        self.id = id
        self.tweets = []
        self.user_type = user_type
        self.followers = []
        self.followers_count = None
        self.following_count = None

    @staticmethod
    def create_user(filename, tweet_list, user_type):
        id = filename.split('\\')[-1].split('.')[0]
        U = User(id, user_type)
        U.tweets = [Tweet(tweet, U) for tweet in tweet_list]
        return U

