import fetcher as fet

def read_file(filename):

    user_list = []

    with open(filename, 'r') as readfile:

        next(readfile)
        for line in readfile:

            comps = line.split()
            user_id = str(comps[0]).replace(',','')
            user_is = 'human'
            user_list.append((user_id, user_is))

    return user_list

def rf_helper(filename):
    r = read_file('datasets/cresci/'+ filename +'/users.csv')
    s = fet.get_legit_users(r)
    conn = fet.create_connection('users.db')
    fet.users_to_db(conn, s, filename)
    conn.close()
    
    print(s)

if __name__ == "__main__":
    #rf_helper('social2')
    #rf_helper('social3')
    #rf_helper('trad1')
    #rf_helper('trad2')
    #rf_helper('trad3')
    #rf_helper('trad4')
    rf_helper('human')