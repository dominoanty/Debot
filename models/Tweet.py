"""
Module for Tweet and any subsequent functions that the model might require

"""

class Tweet:
    """ Model class for a Tweet. """

    def __init__(self):
        self.id = None
        self.text = None
        self.time = None
        self.is_rt = None
        self.user = None