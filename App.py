"""Currently, the main app which makes models from data"""

import json
import logging
import pickle
import os
from models.User import User, UserType
from models.Tweet import Tweet
# from utils.logging import LogMixin

class UserMaker():

    def __init__(self):

        self.users = []

    def scan_dir(self, directory, user_type):
        for filename in os.listdir(directory):
            self.users.append(self.load_from_file(
                os.path.join(directory, str(filename)),
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
    option = None
    while option is not '3':
        print("1. Load data from json files (also pickles)")
        print("2. Load data from pickled  ")
        print("3. Play around with data")
        print("You choose : ")
        option = input()

        if option == '1':
            UM.scan_dir(os.path.join(os.path.dirname(__file__), 'utils\\bot\\'), UserType.BOT)
            with open(os.path.join(os.path.dirname(__file__), 'data\\users.dat'), mode='wb') as file:
                pickle.dump(UM, file)
            print("Load and pickle success")
        
        elif option == '2':
            try:
                with open(os.path.join(os.path.dirname(__file__), 'data\\users.dat'), mode='rb') as file:
                    UM = pickle.load(file)
            except EOFError as E:
                print(E)
            
        
            

    #UM.scan_dir('data\\human4\\', UserType.HUMAN)


