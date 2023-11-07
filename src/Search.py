from Connection import Connection
import os
import math
from Setup import Setup
from Login import Login
from Test import Test


class Search:
    @staticmethod
    def search_for_tweets() -> None:
        """This function prompts the user for keywords to search for and displays the results.
            It also provides various options for interacting with the results.
        """
        keywords = []
        while len(keywords) == 0:
            keywords = input(
                "Enter keywords to search for (separate multiple keywords with spaces): ").strip().lower().split()

        conditions = []
        params = []
        tables = set(["tweets t", "users u"])
        for keyword in keywords:
            if keyword.startswith("#"):
                tables.add("mentions m")
                term = keyword[1:]
                conditions.append("(LOWER(m.term) = ? AND m.tid = t.tid)")
                params.append(term)
            else:
                conditions.append("LOWER(t.text) LIKE ?")
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

        Search.interact(result_list, 5, [
            "scrollup", "scrolldown", "viewinfo", "reply", "retweet"], 'tweet')

    @staticmethod
    def search_for_users() -> None:
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

        column_names = [description[0]
                        for description in Connection.cursor.description]

        result_list = []
        for row in results:
            row_dict = dict(zip(column_names, row))
            result_list.append(row_dict)

        Search.interact(result_list, 5, [
                        "scrollup", "scrolldown", "select"], 'user')

    @staticmethod
    def interact(lst: [dict], num_display: int, additional_options: [str], item_type: str) -> None:
        """This function provides various options for interacting with the results of a search

        Parameters:
            lst (list of dictionaries): A list of tweet objects
            num_display (int): The number of tweets to display per page
            additional_options (list of strings): A list of additional options to display
            item_type (string): The type of item being displayed (tweet or user)
        """
        offset = 0
        print_options = True

        while True:
            if print_options:
                Search.print_item(lst, num_display, offset, item_type)

            cmd = input(">>> ").strip().lower().split()
            if len(cmd) < 1:
                print("INVALID Command -_-")
                continue
            print_options = True

            from Shell import Shell
            if cmd[0] in Shell.get_main_options():
                Shell.main_menu_do(
                    cmd[0], additional_options)
                if (cmd[0] != 'help'):
                    return
                else:
                    print_options = False
                    continue
            elif cmd[0] == 'scrolldown' and len(cmd) == 1:
                if offset + num_display < len(lst):
                    offset += num_display
            elif cmd[0] == 'scrollup' and len(cmd) == 1:
                offset = max(offset - num_display, 0)
            elif cmd[0] == 'reply' and item_type == 'tweet' and len(cmd) == 2:
                print_options = False
                tid = Search.listnum_to_tid(lst, cmd[1])
                if not tid:
                    print("INVALID id")
                    continue
                from ComposeTweet import ComposeTweet
                ComposeTweet.createTweet(tid)
            elif cmd[0] == 'retweet' and item_type == 'tweet' and len(cmd) == 2:
                print_options = False
                tid = Search.listnum_to_tid(lst, cmd[1])
                if not tid:
                    print("INVALID id")
                    continue
                from ComposeTweet import ComposeTweet
                ComposeTweet.createRetweet(tid)
            elif cmd[0] == 'viewinfo' and item_type == 'tweet' and len(cmd) == 2:
                print_options = False
                tid = Search.listnum_to_tid(lst, cmd[1])
                if not tid:
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

    @staticmethod
    def listnum_to_tid(lst, option_id) -> int:
        try:
            index = int(option_id)
            if index > len(lst)+1 or index < 1:
                return 0
            return int(lst[index-1]['tid'])
        except:
            return 0

    @staticmethod
    def print_item(lst: [dict], num_display: int, offset: int, item_type: str) -> None:
        """This function prints a list of tweets or users

        Parameters:
            lst (list of dictionaries): A list of tweet objects
            num_display (int): The number of tweets to display per page
            offset (int): The number of tweets to skip
            item_type (string): The type of item being displayed (tweet or user)
        """
        if len(lst) == 0:
            print("No results found!")
            print()
            return

        print("="*80)
        if item_type == 'tweet':
            for idx, item in enumerate(lst[offset:offset + num_display]):
                print(f"{idx+offset+1}]")
                print(f"\t{item['name']} (+{item['writer']})")
                print(f"\t{item['text']}")
                print()
                print(f"\t{item['tdate']}")
                print()
                print("="*80)
        elif item_type == 'user':
            for idx, item in enumerate(lst[offset:offset + num_display]):
                print(f"{idx+offset+1}]")
                print(f"\t+{item['usr']}")
                print(f"\t{item['name']}")
                print(f"\t{item['city']}")
                print()
                print("="*80)
        print(
            f"Showing page {math.ceil(offset / num_display) + 1} of {max(math.ceil(len(lst)/num_display),1)}")
        print()


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
    # Search.search_for_users()
    Search.search_for_tweets()

    Connection.close()
