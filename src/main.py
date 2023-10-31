import sqlite3
import os
from Login import Login

connection = None
cursor = None


def connect(path):
    global connection, cursor

    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute(' PRAGMA foreign_keys=ON; ')
    connection.commit()
    return


def drop_tables():
    global connection, cursor

    drop_includes = "DROP TABLE IF EXISTS includes; "
    drop_lists = "DROP TABLE IF EXISTS lists; "
    drop_retweets = "DROP TABLE IF EXISTS retweets; "
    drop_mentions = "DROP TABLE IF EXISTS mentions; "
    drop_hashtags = "DROP TABLE IF EXISTS hashtags; "
    drop_tweets = "DROP TABLE IF EXISTS tweets; "
    drop_follows = "DROP TABLE IF EXISTS follows; "
    drop_users = "DROP TABLE IF EXISTS users; "

    cursor.execute(drop_includes)
    cursor.execute(drop_lists)
    cursor.execute(drop_retweets)
    cursor.execute(drop_mentions)
    cursor.execute(drop_hashtags)
    cursor.execute(drop_tweets)
    cursor.execute(drop_follows)
    cursor.execute(drop_users)


def define_tables():
    global connection, cursor

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

    cursor.execute(users_table)
    cursor.execute(follows_table)
    cursor.execute(tweets_table)
    cursor.execute(hashtags_table)
    cursor.execute(mentions_table)
    cursor.execute(retweets_table)
    cursor.execute(lists_table)
    cursor.execute(includes_table)
    connection.commit()

    return


def main():
    global connection, cursor

    path = os.path.dirname(os.path.realpath(__file__)) + "/data.db"
    connect(path)
    drop_tables()
    define_tables()

    Login.set_connection(connection, cursor)
    Login.enter_user()
    user = Login.login()


if __name__ == "__main__":
    main()
