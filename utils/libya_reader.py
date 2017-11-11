import fetcher as fet

def read_file(filename):

    user_list = []

    with open(filename, 'r') as readfile:

        for line in readfile:

            comps = line.split()
            user_is = comps[0]
            user_id = comps[1]
            user_list.append((user_id, user_is))

    return user_list

if __name__ == "__main__":
    r = read_file('datasets/libya/libya.txt')
    s = fet.get_legit_users(r)
    conn = fet.create_connection('users.db')
    fet.users_to_db(conn, s, 'libya')
    conn.close()
    
    print(s)