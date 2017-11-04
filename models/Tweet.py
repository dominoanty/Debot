"""
Module for Tweet and any subsequent functions that the model might require

"""

class Tweet:
    """ Model class for a Tweet. """

    def __init__(self, tweet, user):
        try:
            self.id = tweet["id"]
            self.text = tweet["text"]
            self.time = tweet["created_at"]
            self.is_rt = tweet["retweeted"]
            self.user = user
        except ValueError as VE:
            return None