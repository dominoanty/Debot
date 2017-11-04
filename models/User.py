"""User module containing User Model and UserType Enum """
from enum import Enum
from . import Tweet 


class UserType(Enum):
    """The type of the user. Currently Human -> 0 and Bot -> 1"""


    HUMAN = 0
    BOT = 1

class User:
    """Model class that holds the information for a user."""

    def __init__(self, user_type):
        self.id = None
        self.tweets = []
        self.user_type = user_type
        self.followers = []
