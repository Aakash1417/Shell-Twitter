import sqlite3


class Setup:
    connection = None
    cursor = None

    @staticmethod
    def is_connected():
        return Setup.connection is not None and Setup.cursor is not None


    @staticmethod
    def connect(path):
        Setup.connection = sqlite3.connect(path)
        Setup.cursor = Setup.connection.cursor()
        Setup.cursor.execute(' PRAGMA foreign_keys=ON; ')
        Setup.connection.commit()


    @staticmethod
    def drop_tables():
        drop_includes = "DROP TABLE IF EXISTS includes; "
        drop_lists = "DROP TABLE IF EXISTS lists; "
        drop_retweets = "DROP TABLE IF EXISTS retweets; "
        drop_mentions = "DROP TABLE IF EXISTS mentions; "
        drop_hashtags = "DROP TABLE IF EXISTS hashtags; "
        drop_tweets = "DROP TABLE IF EXISTS tweets; "
        drop_follows = "DROP TABLE IF EXISTS follows; "
        drop_users = "DROP TABLE IF EXISTS users; "

        Setup.cursor.execute(drop_includes)
        Setup.cursor.execute(drop_lists)
        Setup.cursor.execute(drop_retweets)
        Setup.cursor.execute(drop_mentions)
        Setup.cursor.execute(drop_hashtags)
        Setup.cursor.execute(drop_tweets)
        Setup.cursor.execute(drop_follows)
        Setup.cursor.execute(drop_users)


    def define_tables():
        users_table = """
        CREATE TABLE users (
        usr         TEXT,
        pwd         TEXT,
        name        TEXT,
        email       TEXT,
        city        TEXT,
        timezone    REAL,
        PRIMARY KEY (usr)
        );
        """

        follows_table = """
        CREATE TABLE follows (
        flwer       INTEGER,
        flwee       INTEGER,
        start_date  DATE,
        PRIMARY KEY (flwer, flwee),
        FOREIGN KEY (flwer) REFERENCES users(usr),
        FOREIGN KEY (flwee) REFERENCES users(usr)
        );
        """

        tweets_table = """
        CREATE TABLE tweets (
        tid         INTEGER,
        writer      INTEGER,
        tdate       DATE,
        text        TEXT,
        replyto     INTEGER,
        PRIMARY KEY (tid),
        FOREIGN KEY (writer) REFERENCES users(usr),
        FOREIGN KEY (replyto) REFERENCES tweets(tid)
        );
        """

        hashtags_table = """
        CREATE TABLE hashtags (
        term        TEXT,
        PRIMARY KEY (term)
        );
        """

        mentions_table = """
        CREATE TABLE mentions (
        tid         INTEGER,
        term        TEXT,
        PRIMARY KEY (tid, term),
        FOREIGN KEY (tid) REFERENCES tweets(tid),
        FOREIGN KEY (term) REFERENCES hashtags(term)
        );
        """

        retweets_table = """
        CREATE TABLE retweets (
        usr         INTEGER,
        tid         INTEGER,
        rdate       DATE,
        PRIMARY KEY (usr, tid),
        FOREIGN KEY (usr) REFERENCES users(usr),
        FOREIGN KEY (tid) REFERENCES tweets(tid)
        );
        """

        lists_table = """
        CREATE TABLE lists (
        lname       TEXT,
        owner       INTEGER,
        PRIMARY KEY (lname),
        FOREIGN KEY (owner) REFERENCES users(usr)
        );
        """

        includes_table = """
        CREATE TABLE includes (
        lname       TEXT,
        member      INTEGER,
        PRIMARY KEY (lname, member),
        FOREIGN KEY (lname) REFERENCES lists(lname),
        FOREIGN KEY (member) REFERENCES users(usr)
        );
        """

        Setup.cursor.execute(users_table)
        Setup.cursor.execute(follows_table)
        Setup.cursor.execute(tweets_table)
        Setup.cursor.execute(hashtags_table)
        Setup.cursor.execute(mentions_table)
        Setup.cursor.execute(retweets_table)
        Setup.cursor.execute(lists_table)
        Setup.cursor.execute(includes_table)
        Setup.connection.commit()
