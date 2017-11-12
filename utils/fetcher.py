import twitter_conf as tc
from tweepy import TweepError
import sqlite3
from sqlite3 import Error
import time
import csv
import json


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return None


def reporter(function, data, limit=100):
    """
        reporter function that chunks a function into set limits 
        and prints status to keep you informed
        :param function : The function which takes a single parameter 
                          and returns a list of results
        :param data: The data as input to the function
        :param limit: chunk limit
        :return: The concatenated results from all chunks
    """
    results = []
    while data != []:
        get_data = data[:min(limit, len(data))]
        print(" Percentage  " + str(len(get_data) / len(data)))
        try:
            results += function(get_data)
            data = data[min(limit, len(data)):]
        except TweepError as E:
            if '17' in str(E):
                data = data[min(limit, len(data)):]
            else:
                print(E)
                time.sleep(60 * 15)
        except StopIteration:
            break
    return results


def lookup_users(data):
    print("Entered : " + str(len(data)))
    users = tc.api.lookup_users(user_ids=data)
    print("Exit :" + str(len(users)))
    return users


def get_legit_users(user_list):
    """
        Takes input as tuple(user, user_status) and returns
        a filtered list for english users that stiill exist
        :param user_list: user, user_status tuple list
    """
    user_status = {}

    for user, status in user_list:
        user_status[user] = status
    print(user_status)

    result = reporter(
        lookup_users, [user for user, status in user_list], limit=100)

    print([user.lang for user in result])
    real_result = [(str(user.id), user_status[str(user.id)])
                   for user in result if 'en' in user.lang]
    with open('temp.txt', 'w') as outfile:
        for result in real_result:
            outfile.write(','.join(result))
            outfile.write('\n')
    return real_result


def get_tweet_for_user(user):
    user_id, user_is, source, _ = user
    print("getting tweets for %s" % (user_id))
    alltweets = []

    try:
        new_tweets = tc.api.user_timeline(user_id=user_id, count=200, include_rts=True)
        alltweets.extend(new_tweets)

        oldest = alltweets[-1].id - 1

        while len(new_tweets) > 0 and len(alltweets) <= 1000:

            new_tweets = tc.api.user_timeline(
                user_id=user_id, count=200, max_id=oldest)

            alltweets.extend(new_tweets)
            oldest = alltweets[-1].id - 1

        with open(user_is + '/' + user_id + '.json', 'w') as writefile:
            writefile.write(json.dumps([status._json for status in alltweets]))
    except TweepError as TE:
        if 'ver' in str(TE):
            return False
        print(TE)
        return None
    except IndexError as IE:
        return True


    return True
    # write the csv
    # with open('%s_tweets.csv' % user_id, 'w') as f:
        # writer = csv.writer(f)
        # writer.writerow(["id", "created_at", "text"])
        # writer.writerows(outtweets)


def users_to_db(conn, user_list, source):
    cursor = conn.cursor()
    for user, status in user_list:
        cursor.execute('insert into users values(?,?,?,\'false\')',
                       (user, status, source,))
    conn.commit()

def set_processed(conn, user_id):
    cur = conn.cursor()
    statement = "UPDATE users SET processed=\'true\' where id=\'" + user_id + "\'" 
    cur.execute(statement)
    conn.commit()

def db_to_users(conn, user_type=None, source=None):

    statement = "SELECT * FROM users WHERE processed=\'false\' "
    cur = conn.cursor()

    if user_type == 'bot':
        statement += " and status = \'bot\'"
    elif user_type == 'human':
        statement += " and status = \'human\'"
    
    if source is not None:
        statement += " and source = \'" + source + "\'"
    cur.execute(statement)
    rows = cur.fetchall()
    return rows
