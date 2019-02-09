"""
Module for Tweet and any subsequent functions that the model might require

"""
import params
from .ArabicError import ArabicError


class Tweet:
    """ Model class for a Tweet. """

    def __init__(self, tweet, user):
        try:
            self.id = tweet["id"]
            self.text = tweet["text"]

            if params.ARABIC_TESTER.search(self.text) is not None:
                raise ArabicError("Text contains arabic!")

            self.time = tweet["created_at"]
            self.user = user
            self.vector_form = None

            if "retweeted_status" in tweet:
                self.is_rt = True
            else:
                self.is_rt = False

        except ValueError as VE:
            return None
