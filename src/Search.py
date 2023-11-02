from Connection import Connection
import os
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
        tables = set(["tweets t"])
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
            SELECT DISTINCT t.tid, t.writer, t.tdate, t.text
            FROM {table_clause}
            WHERE {where_clause}
            ORDER BY t.tdate DESC;"""
        print(query)
        print(params)

        Connection.cursor.execute(query, params)
        results = Connection.cursor.fetchall()
        print(results)

    @staticmethod
    def display_tweets(twts):
        pass


def AddTestData():
    insert_query = f"""INSERT INTO Users VALUES 
                    (1, 'password1', 'User1', 'user1@example.com', 'City1', 1.0),
                    (2, 'password2', 'User2', 'user2@example.com', 'City2', 2.0),
                    (3, 'password3', 'User3', 'user3@example.com', 'City3', 3.0);"""
    Connection.cursor.executescript(insert_query)

    insert_query = f"""INSERT INTO tweets (tid, writer, tdate, text, replyto) VALUES 
                    (1, 1, 2023-10-27, 'This is a #test tweet.', NULL),
                    (2, 2, 2023-3-27, 'This is #another tweet that I am reply to someone else with', 1);"""
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
    print("done")


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
