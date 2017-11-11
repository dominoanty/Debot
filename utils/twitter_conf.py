import tweepy
import json
import time

consumer_key = "JmQr1YT32tlSq5wxBKkjKc2lp"
consumer_secret="3vncTmgwfG9l3r1Mr4As6qDwIZ6JbeXnabcGHWCtQhA3kr2sCS"
access_token = "30849653-NmqW8iMe6WLOuLhtmnJeZZFSjDw1Xxm07tL23KuRW"
access_token_secret = "UHZbI3NqsvZBqvtxc8VP9fhjzbG5lfQByP9rDmdFmrHzo"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)
