"""Currently, the main app which makes models from data"""

import json
import logging
from os import listdir, path
from models.User import User, UserType
from models.Tweet import Tweet
# from utils.logging import LogMixin

class UserMaker():

    def __init__(self):

        self.users = []

    def scan_dir(self, directory, user_type):
        for filename in listdir(directory):
            self.users.append(self.load_from_file(
                path.join(directory, str(filename)),
                user_type
            ))
        self.users = list(filter(lambda x : True if x is not None else False, self.users))

    def load_from_file(self, filename, user_type):
        print("Loading file : " + filename)
        with open(filename) as data_file:
            tweet_list = json.load(data_file)
            print("Length of tweet list : " + str(len(tweet_list)))
            if len(tweet_list) < 100:
                return None
            else:
                return User.create_user(filename, tweet_list, user_type)

if __name__ == "__main__":
    UM = UserMaker()
    UM.scan_dir('data\\bot4\\', UserType.BOT)
    UM.scan_dir('data\\human4\\', UserType.HUMAN)


