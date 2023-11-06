from Connection import Connection
import os
import math
from Setup import Setup
from Login import Login
from Test import Test


class Search:
    @staticmethod
    def search_for_tweets():
        keywords = input(
            "Enter keywords to search for (separate multiple keywords with spaces): ").strip().split()

        conditions = []
        params = []
        tables = set(["tweets t", "users u"])
        for keyword in keywords:
            if keyword.startswith("#"):
                tables.add("mentions m")
                term = keyword[1:]
                conditions.append("(m.term = ? AND m.tid = t.tid)")
                params.append(term)
            else:
                conditions.append("t.text LIKE ?")
                params.append('%' + keyword + '%')

        table_clause = ", ".join(tables)
        where_clause = " OR ".join(conditions)

        query = f"""
            SELECT DISTINCT u.name, t.tid, t.writer, t.tdate, t.text
            FROM {table_clause}
            WHERE ({where_clause})
            AND u.usr = t.writer
            ORDER BY t.tdate DESC;"""

        Connection.cursor.execute(query, params)
        results = Connection.cursor.fetchall()

        column_names = [description[0]
                        for description in Connection.cursor.description]
        result_list = []
        for row in results:
            row_dict = dict(zip(column_names, row))
            result_list.append(row_dict)

        Search.interact_with_tweet(result_list, 5)

    @staticmethod
    def interact_with_tweet(twts, num_display):
        # scrollUP
        # scrolldown
        # retweet
        # reply
        # cancel
        offset = 0
        print_options = True
        from Shell import Shell
        Shell.current_state = 'viewTweet'
        while True:
            if print_options:
                print("="*32)
                for tweet in twts[offset:offset + num_display]:
                    print()
                    print(f"ID: {tweet['tid']}")
                    print(f"    {tweet['name']} (+{tweet['writer']})")
                    print(f"    {tweet['text']}")
                    print(f"    {tweet['tdate']}")
                    print()
                    print("="*32)

                print(
                    f"Showing page {math.ceil(offset / num_display) + 1} of {max(math.ceil(len(twts)/num_display),1)}")
                print()

            cmd = input(">>> ").strip().lower().split()

            print_options = True

            if cmd[0] in Shell.get_options():
                Shell.main_menu_do(cmd[0])
                if (cmd[0] not in ['help', 'clear']):
                    Shell.current_state = None
                    return
                else:
                    print_options = False
                    continue
            elif cmd[0] == 'scrolldown':
                if offset + num_display < len(twts):
                    offset += num_display
            elif cmd[0] == 'scrollup':
                offset = max(offset - num_display, 0)
            elif cmd[0] == 'reply':
                # Implement reply functionality here
                pass
            elif cmd[0] == 'retweet':
                # Implement retweet functionality here
                pass
            else:
                print("INVALID Command -_-")
                continue
            
    @staticmethod
    def search_for_users():
        """Searches for users whose name or city match a keyword
        
        Args:
            None

        Returns:
            List of users whose name or city match
        """
        assert Connection.is_connected()
        keyword = input("Enter a keyword to search users for:")
        
        # users whose name match are shown in ascending order of name length first
        # then, remaining users by ascending order of city length
        query = """
            SELECT DISTINCT usr, name, city
            FROM users
            WHERE LOWER(name) LIKE '%' || LOWER(?) || '%' 
            OR LOWER(city) LIKE '%' || LOWER(?) || '%'
            ORDER BY
                (CASE
                    WHEN LOWER(name) LIKE '%' || LOWER(?) || '%' THEN 1
                    ELSE 2
                END),
                (CASE
                    WHEN LOWER(name) LIKE '%' || LOWER(?) || '%' THEN LENGTH(name)
                    ELSE LENGTH(city)
                END);"""
        Connection.cursor.execute(query, (keyword, keyword, keyword, keyword))
        results = Connection.cursor.fetchall()
        
        column_names = [description[0] for description in Connection.cursor.description]
        
        result_list = []
        for row in results:
            row_dict = dict(zip(column_names, row))
            result_list.append(row_dict)
            
        Search.interact_with_user(result_list, 5)

    
    @staticmethod
    def interact_with_user(users, num_display):
        offset = 0
        print_options = True
        from Shell import Shell
        Shell.current_state = 'viewTweet'
        
        while True:
            if print_options:
                print("="*32)
                for user in users[offset:offset + num_display]:
                    print()
                    print(f"ID: {user['usr']}")
                    print(f"    {user['name']}")
                    print(f"    {user['city']}")
                    print()
                    print("="*32)

                print(
                    f"Showing page {math.ceil(offset / num_display) + 1} of {max(math.ceil(len(users)/num_display),1)}")
                print()

            cmd = input(">>> ").strip().lower().split()

            print_options = True

            if cmd[0] in Shell.get_options():
                Shell.main_menu_do(cmd[0])
                if (cmd[0] not in ['help', 'clear']):
                    Shell.current_state = None
                    return
                else:
                    print_options = False
                    continue
            elif cmd[0] == 'scrolldown':
                if offset + num_display < len(users):
                    offset += num_display
            elif cmd[0] == 'scrollup':
                offset = max(offset - num_display, 0)
            else:
                print("INVALID Command -_-")
                continue
        
        pass


def AddTestData():
    insert_query = f"""INSERT INTO Users VALUES 
                    (1, 'password1', 'User1', 'user1@example.com', 'City1', 1.0),
                    (2, 'password2', 'User2', 'user2@example.com', 'City2', 2.0),
                    (3, 'password3', 'User3', 'user3@example.com', 'City3', 3.0),
                    (4, 'password4', 'User4', 'user4@example.com', 'City4', 4.0),
                    (5, 'password5', 'User5', 'user5@example.com', 'City5', 5.0),
                    (6, 'password6', 'User6000', 'user6@example.com', 'City6', 6.0),
                    (7, 'password7', 'User', 'user7@example.com', 'UserCity', 7.0),
                    (8, 'password8', 'Sam1', 'sam1@example.com', 'UserCity1', 8.0),
                    (9, 'password9', 'Sam2', 'sam2@example.com', 'UserCity12', 9.0),
                    (10, 'password10', 'User10', 'user10@example.com', 'UserCity123', 10.0),
                    (11, 'password11', 'User100', 'user11@example.com', 'City', 11.0),
                    (12, 'password12', 'Sam', 'user12@example.com', 'SamCity', 12.0),
                    (13, 'password13', 'Bam', 'user13@example.com', 'BamCity', 13.0);"""
    Connection.cursor.executescript(insert_query)

    insert_query = f"""INSERT INTO tweets (tid, writer, tdate, text, replyto) VALUES 
                    (1, 1, '2023-01-27', 'This is a #test tweet.', NULL),
                    (2, 2, '2023-02-27', 'This is #another tweet that I am reply to someone else with', NULL),
                    (3, 1, '2023-03-27', 'test of 3', NULL),
                    (4, 1, '2023-04-27', 'test of 3', NULL),
                    (5, 1, '2023-05-27', 'test of 3', NULL),
                    (6, 1, '2023-06-27', 'test of 3', NULL),
                    (7, 1, '2023-07-27', 'test of 3', NULL);"""
    Connection.cursor.executescript(insert_query)

    hashtags_data = [
        ('test',),
        ('another',),
        ('thingy',),
    ]
    Connection.cursor.executemany(
        "INSERT INTO hashtags VALUES (?)", hashtags_data)

    mentions_data = [
        (1, 'test'),
        (1, 'another'),
        (2, 'another'),
        (3, 'another'),
        (4, 'another'),
        (5, 'another'),
        (6, 'another'),
        (7, 'another'),
    ]
    Connection.cursor.executemany(
        "INSERT INTO mentions VALUES (?,?)", mentions_data)
    Connection.connection.commit()


if __name__ == "__main__":
    path = os.path.dirname(os.path.realpath(__file__)) + "/data.db"
    Connection.connect(path)

    Setup.drop_tables()
    Setup.define_tables()
    # Test.insert_test_data()
    AddTestData()

    Login.userID = 2
    Search.search_for_users()
    # Search.search_for_tweets()

    Connection.close()
