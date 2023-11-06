from Connection import Connection
import os
import math
from Setup import Setup
from Login import Login
from Test import Test


class Search:
    @staticmethod
    def search_for_tweets():
        """This function prompts the user for keywords to search for and displays the results.
            It also provides various options for interacting with the results.
        """
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
        """This function displays a list of tweets and providing various options for interacting with them.
        It takes user input to navigate through the tweet and perform actions.

        Parameters:
            twts (list of dictionaries): A list of tweet objects
            num_display (int): The number of tweets to display per page
        """
        offset = 0
        print_options = True
        from Shell import Shell
        while True:
            if print_options:
                print("="*32)
                for idx, tweet in enumerate(twts[offset:offset + num_display]):
                    print(f"{idx+offset+1}]")
                    print(f"\t{tweet['tid']}")
                    print(f"\t{tweet['name']} (+{tweet['writer']})")
                    print(f"\t{tweet['text']}")
                    print()
                    print(f"\t{tweet['tdate']}")
                    print()
                    print("="*32)

                print(
                    f"Showing page {math.ceil(offset / num_display) + 1} of {max(math.ceil(len(twts)/num_display),1)}")
                print()

            cmd = input(">>> ").strip().lower().split()

            print_options = True

            if cmd[0] in Shell.get_main_options():
                Shell.main_menu_do(
                    cmd[0], ["scrollup", "scrolldown", "select", "reply", "retweet"])
                if (cmd[0] not in ['help', 'clear']):
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
            elif cmd[0] == 'select':
                print_options = False
                try:
                    index = int(cmd[1])
                    if index > len(twts)+1 or index < 1:
                        print("INVALID id")
                        continue
                    tid = twts[index-1]['tid']
                except:
                    print("INVALID id")
                    continue
                Connection.cursor.execute(
                    "SELECT COUNT(*) FROM retweets WHERE tid = ?", (tid,))
                retweets_count = Connection.cursor.fetchone()[0]

                Connection.cursor.execute(
                    "SELECT COUNT(*) FROM tweets WHERE replyto = ?", (tid,))
                replies_count = Connection.cursor.fetchone()[0]

                print(
                    f"Tweet +{tid} has {retweets_count} retweets and {replies_count} replies")
            else:
                print("INVALID Command -_-")
                continue


def AddTestData():
    insert_query = f"""INSERT INTO Users VALUES 
                    (1, 'password1', 'User1', 'user1@example.com', 'City1', 1.0),
                    (2, 'password2', 'User2', 'user2@example.com', 'City2', 2.0),
                    (3, 'password3', 'User3', 'user3@example.com', 'City3', 3.0);"""
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

    Search.search_for_tweets()

    Connection.close()
