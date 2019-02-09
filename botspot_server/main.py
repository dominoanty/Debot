from flask import Flask, jsonify
import tweepy
from tweepy import TweepError
import json
import time
from keras.models import load_model
from ..utils import per_user

app = Flask(__name__)

consumer_key = "JmQr1YT32tlSq5wxBKkjKc2lp"
consumer_secret="3vncTmgwfG9l3r1Mr4As6qDwIZ6JbeXnabcGHWCtQhA3kr2sCS"
access_token = "30849653-NmqW8iMe6WLOuLhtmnJeZZFSjDw1Xxm07tL23KuRW"
access_token_secret = "UHZbI3NqsvZBqvtxc8VP9fhjzbG5lfQByP9rDmdFmrHzo"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)
class known_users:
    def __init__(self):
        users = []
ku = known_users()

def get_tweets_for_user(user_id):

    alltweets = []
    try:
        new_tweets = api.user_timeline(user_id=user_id, count=100, include_rts=True)
        alltweets.extend(new_tweets)

        # oldest = alltweets[-1].id - 1

        # while len(new_tweets) > 0 and len(alltweets) <= 400:

        #     new_tweets = api.user_timeline(
        #         user_id=user_id, count=200, max_id=oldest)

        #     alltweets.extend(new_tweets)
        #     oldest = alltweets[-1].id - 1

        return alltweets
    except TweepError as TE:
        if 'ver' in str(TE):
            return False
        print(TE)
        return None
    except IndexError as IE:
        print(IE)
        return None

@app.route("/<user_id>", methods=['GET'])
def check_user(user_id):
    print("Received request for + " + user_id)
    scores = []
    scores = per_user.pass_through_model(user_id)
    print(scores)
    human_percent = scores[0][0][0] + scores[1][0][0] + scores[2][0][0]
    human_percent /= 3
    bot_percent = scores[0][0][1] + scores[1][0][1] + scores[2][0][1]
    bot_percent /= 3
    result = "human" if human_percent > bot_percent else "bot"
    confidence = human_percent  if human_percent > bot_percent else bot_percent
    print("confidence "+ str(float(confidence)))
    return jsonify({"user_id" : user_id, "result" : result, "confidence" : round(float(confidence),2)})
    # except:
    #     return jsonify({"user_id" : user_id, "result" : "bot", "confidence" : "0.95"})

known_users = []
@app.route("/<user_id>/<user_type>", methods=['POST'])
def assert_user(user_id, user_type):
    print("received report for" + user_id)
    print(user_id, user_type)
    ku.users.append((user_id, 0 if user_type is "human" else 1))
    if(len(ku.users) > 31):
        per_user.update_model(ku.users)
        ku.users = []
    return ""

@app.route("/")
def hello():
    return "Hello World!"