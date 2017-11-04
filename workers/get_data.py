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
user_count = 0
line_count = 0

with open('honeypot.txt', 'r') as readfile:
    
    for line in readfile:

        line_count+=1
        if line_count < 3:
            continue

        comps = line.split()
        user_is = comps[0]
        user_id = comps[1]
        status_list = []
        while status_list is not []:
            try:
                for page in tweepy.Cursor(api.user_timeline, user_id=user_id, include_rts=True).items(1000):
                    status_list.append(page)
            
            except tweepy.TweepError as TE:
                print(TE)
                if "401" in str(TE.response):
                    print("User Suspended")
                else:
                    print("Waiting 5 Minutes")
                    time.sleep(60*15)

        if len(status_list) < 200:
            continue

        user_count += 1
        with open(user_is + '/' + user_id + '.json', 'w') as writefile:
            writefile.write(json.dumps([status._json for status in status_list]))

        print("Finished processing id = " + user_id)
        print("Count is now " + str(line_count))
        
        

# with open('honeypot.txt', 'r') as readfile:

#     for line in readfile:

#         # if count < 5354:
#         #     count += 1
#         #     continue

#         comps = line.split()
#         user_is = comps[0]
#         user_id = comps[1]
#         tweet_list = comps[2:]
#         tweets = []
#         count+=1

#         while tweet_list != []:
#             get_data = tweet_list[:min(100, len(tweet_list))]
#             print(len(get_data))
#             try:
#                 tweets += api.statuses_lookup(get_data)
#                 tweet_list = tweet_list[min(100,len(tweet_list)):]
#             except tweepy.TweepError:
#                 time.sleep(60 * 15)
#                 continue
#             except StopIteration:
#                 break

#         with open(user_is + '/' + user_id + '.json', 'w') as writefile:
#             writefile.write(json.dumps([tweet._json for tweet in tweets]))
    
#         print("Finished processing id = " + user_id)
#         print("Count is now " + str(count))
        
