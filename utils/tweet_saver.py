import fetcher

if __name__ == '__main__':
    conn = fetcher.create_connection('users.db')
    user_list = fetcher.db_to_users(conn, user_type='bot')
    for user in user_list:
        op = fetcher.get_tweet_for_user(user)
        if op == True:
            fetcher.set_processed(conn, user[0])