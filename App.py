"""Currently, the main app which makes models from data"""

import params
import json
import logging
import pickle
import os
from random import shuffle
from models.User import User, UserType, UserData
from models.Tweet import Tweet
# from utils.logging import LogMixin

class UserMaker():

    def __init__(self):

        self.users = []

    def scan_dir(self, directory, user_type):
        '''
        Given a directory and user type, for each file, calls load_from_file (creates user and pickles),
        and then creates list of UserData[] objects.
        '''
        for filename in os.listdir(directory):
            new_user = self.load_from_file(
                os.path.join(directory, str(filename)),
                user_type)
            
            self.users.append(new_user)
        self.users = list(filter(lambda x : True if x is not None else False, self.users))

    def load_from_file(self, filename, user_type):
        '''
        Given a file and usertype, loads the file, pickles it and then returns UserData only. 
        '''
        print("Loading file : " + filename)
        with open(filename) as data_file:
            tweet_list = json.load(data_file)
            print("Length of tweet list : " + str(len(tweet_list)))
            if len(tweet_list) < 100:
                return None
            else:
                return User.create_user(filename, tweet_list, user_type) # Returns None if arabic characters found

class DatasetMaker():
    '''
    Used to create training and test datasets. Balances the ratio of normal : spam tweets in the ratio (params.SPAM_RATIO)
    '''

    def __init__(self, UM):
        self.human_users = list(filter(lambda x: True if x.user_type == UserType.HUMAN
                                       else False, UM.users))
        shuffle(self.human_users)
        self.bot_users = list(filter(lambda x: True if x.user_type == UserType.BOT
                                     else False, UM.users))
        shuffle(self.bot_users)

        self.no_human_tweets = sum([x.num_tweets for x in self.human_users])
        self.no_bot_tweets = sum([x.num_tweets for x in self.bot_users])


        # The ratio of bot : human tweets should be in spam ratio
        self.req_bot_tweets = params.SPAM_RATIO * self.no_human_tweets / (1 - params.SPAM_RATIO)

        # Currently using averages, can be switched to definite amounts later
        self.new_bot_users = []
        self.new_bot_tweets = 0
        for user in self.bot_users:
            self.new_bot_users.append(user)
            self.new_bot_tweets += user.num_tweets
            if self.new_bot_tweets > self.req_bot_tweets:
                break
        
        #self.bot_users = self.bot_users[:len(self.bot_users) - self.less_bots_by]
        self.bot_users = self.new_bot_users
        
        human_div = int(len(self.human_users) * params.TRAIN_RATIO)
        bot_div = int(len(self.bot_users)* params.TRAIN_RATIO )
        
        self.train_users = self.human_users[: human_div]
        self.train_users += self.bot_users[: bot_div]
        self.test_users = self.human_users[human_div : ]
        self.test_users += self.bot_users[bot_div : ]


if __name__ == "__main__":
    UM = UserMaker()
    DM = None
    option = None
    while option is not '3':
        print("1. Load data from json files (also pickles)")
        print("2. Load data from pickled  ")
        print("3. Play around with data")
        print("4. Prepare dataset")
        print("You choose : ")
        option = input()

        if option == '1':
            UM.scan_dir(os.path.join(os.path.dirname(__file__), 'utils\\bot\\'), UserType.BOT)
            UM.scan_dir(os.path.join(os.path.dirname(__file__), 'utils\\human\\'), UserType.HUMAN)
            with open(os.path.join(os.path.dirname(__file__), 'data\\users.dat'), mode='wb') as file:
                pickle.dump(UM, file)
            print("Load and pickle success")
        
        elif option == '2':
            try:
                with open(os.path.join(os.path.dirname(__file__), 'data\\users.dat'), mode='rb') as file:
                    UM = pickle.load(file)
            except EOFError as E:
                print(E)
        elif option == '4':
            DM = DatasetMaker(UM)

            
        
            

    #UM.scan_dir('data\\human4\\', UserType.HUMAN)


