from Connection import Connection
import os
import math
from Setup import Setup
from Login import Login
from Shell import Shell
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

        Search.interact_with_tweet(results, 5)

    @staticmethod
    def interact_with_tweet(twts, num_display):
        # scrollUP
        # scrolldown
        # retweet
        # reply
        # cancel
        offset = 0
        while True:
            print("="*32)
            for tweet in twts[offset:offset + num_display]:
                print()
                print(f"ID: {tweet[1]}")
                print(f"    {tweet[0]} (+{tweet[2]})")
                print(f"    {tweet[-1]}")
                print(f"    {tweet[3]}")
                print()
                print("="*32)

            print(
                f"Showing page {math.ceil(offset / num_display) + 1} of {math.ceil(len(twts)/num_display)}")
            print()

            cmd = input("type the thing bro: ").strip().lower().split()

            if cmd[0] == 'scrolldown':
                offset = min(offset + num_display, len(twts) - 1)
            elif cmd[0] == 'scrollup':
                offset = max(offset - num_display, 0)
            elif cmd[0] == 'reply':
                # Implement reply functionality here using the reply_id
                pass
            elif cmd[0] == 'retweet':
                # Implement retweet functionality here using the retweet_id
                pass
            elif cmd[0] == 'cancel':
                break
            else:
                print("INVALID Command -_-")

            Shell.clear()


def AddTestData():
    insert_query = f"""INSERT INTO Users VALUES 
                    (1, 'password1', 'User1', 'user1@example.com', 'City1', 1.0),
                    (2, 'password2', 'User2', 'user2@example.com', 'City2', 2.0),
                    (3, 'password3', 'User3', 'user3@example.com', 'City3', 3.0);"""
    Connection.cursor.executescript(insert_query)

    insert_query = f"""INSERT INTO tweets (tid, writer, tdate, text, replyto) VALUES 
                    (1, 1, '2023-01-27', 'This is a #test tweet.', NULL),
                    (2, 2, '2023-02-27', 'This is #another tweet that I am reply to someone else with', NULL),
                    (3, 1, '2023-03-27', 'test of 3', NULL);"""
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
        (2, 'thingy'),
    ]
    Connection.cursor.executemany(
        "INSERT INTO mentions VALUES (?,?)", mentions_data)
    Connection.connection.commit()


if __name__ == "__main__":
    path = os.path.dirname(os.path.realpath(__file__)) + "/data.db"
    Connection.connect(path)

    Setup.drop_tables()
    Setup.define_tables()
    # Test.add_mock_users()

    AddTestData()
    Login.userID = 2

    Search.search_for_tweets()

    Connection.close()
