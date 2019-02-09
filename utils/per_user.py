from . import fetcher
from .twitter_conf import api
from ..models.User import User
from tweepy import TweepError
import numpy as np

from keras.models import load_model, Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten, Reshape
from keras.layers.convolutional import Conv1D, MaxPooling1D
from keras.utils import np_utils
from keras.layers.recurrent import LSTM
from keras.models import load_model

batch_size=32
num_epochs=20
num_pool=2
num_filters = 128
conv_kernel_width = 3
conv_kernel_height = 200
lstm_output_size= 70
dropout_rate = 0.1
INPUT_UNITS = 32

from keras.layers import Merge

models = []
for i in range(INPUT_UNITS):
    tmodel = Sequential()
    tmodel.add(Conv1D(num_filters, 
                      conv_kernel_width,
                      padding='same',
                      activation='relu',
                      strides=1,
                      input_shape=(20, 200)))
    tmodel.add(MaxPooling1D(pool_size=20))
    models.append(tmodel)

fmodel = Sequential()
fmodel.add(Merge(models, mode='concat'))
fmodel.add(LSTM(64))
fmodel.add(Dropout(0.1))
fmodel.add(Dense(2))
fmodel.add(Activation('softmax'))
fmodel.compile(loss='binary_crossentropy',
               optimizer='adam',
               metrics=['accuracy'])

fmodel.load_weights("G:\\Programming\\major\\ut_model_weights")

# models = []
# for i in range(INPUT_UNITS):
#     tmodel = Sequential()
#     tmodel.add(Conv1D(num_filters, 
#                       conv_kernel_width,
#                       padding='same',
#                       activation='relu',
#                       strides=1,
#                       input_shape=(20, 200)))
#     tmodel.add(MaxPooling1D(pool_size=20))
#     models.append(tmodel)

# fmodel = Sequential()
# fmodel.add(Merge(models, mode='concat'))
# fmodel.add(Dropout(0.1))
# fmodel.add(Dense(64, activation='relu'))
# fmodel.add(Flatten())
# fmodel.add(Dense(2))
# fmodel.add(Activation('sigmoid'))
# fmodel.compile(loss='binary_crossentropy',
#                optimizer='adam',
#                metrics=['accuracy'])
# fmodel.load_weights("G:\\Programming\\major\\ut_model_weights_nolstm")
def get_tweets_for_user(user_id):
    alltweets = []
    try:
        new_tweets = api.user_timeline(user_id=user_id, count=128, include_rts=True)
        alltweets.extend(new_tweets)
        return alltweets
    except TweepError as TE:
        if 'ver' in str(TE):
            return False
        print(TE)
        return None
    except IndexError as IE:
        print(IE)
        return None

def lookup_user(user):
    user = api.lookup_users(user_ids=[user])
    try: 
        user = user[0]
        if 'en' in user.lang:
            return user
    except IndexError: 
        return None
    return None

def get_user_details(user_id): 
    user = lookup_user(user_id)
    if user is None:
        return None
    else:
        tweet_list = [tweet._json for tweet in get_tweets_for_user(user.id)]
        U = User.create_user_uk(user.id, tweet_list)
        return U

def pass_through_model(id):
    user = get_user_details(id)
    if user is None: 
        return None
    scores = []
    i = 0
    while (i+1)*INPUT_UNITS <= len(user.tweets):
        tweets = user.tweets[i*INPUT_UNITS : min((i+1) * INPUT_UNITS, len(user.tweets))]
        scores.append(fmodel.predict([np.reshape(np.array(tweet.vector_form), (1,20,200)) for tweet in tweets]))
        i+=1 
    return scores

def update_model(known_users):
    users = []
    for temp_user in known_users: 
        try:
            user = get_user_details(temp_user[0])
            i = 0
            while (i+1)*INPUT_UNITS <= len(user.tweets):
                tweets = user.tweets[i*INPUT_UNITS : min((i+1) * INPUT_UNITS, len(user.tweets))]
                fmodel.train_on_batch([np.reshape(np.array(tweet.vector_form), (1,20,200)) for tweet in tweets], [temp_user[1]])
        except:
            pass

if __name__ == '__main__':
    print("Enter the id of user : ")
    id = '30849653'
    user = get_user_details(id)
    fmodel.load_weights("G:\\Programming\\major\\ut_model_weights")
    UNIT_SIZE = 32
    scores = []
    i = 0
    while (i+1)*UNIT_SIZE <= len(user.tweets):
        tweets = user.tweets[i*UNIT_SIZE : min((i+1) * UNIT_SIZE, len(user.tweets))]
        scores.append(fmodel.predict([np.reshape(np.array(tweet.vector_form), (1,20,200)) for tweet in tweets]))
        i+=1 
    print(scores)
