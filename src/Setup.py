from Connection import Connection


class Setup:
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

        Connection.cursor.executescript(drop_includes)
        Connection.cursor.executescript(drop_lists)
        Connection.cursor.executescript(drop_retweets)
        Connection.cursor.executescript(drop_mentions)
        Connection.cursor.executescript(drop_hashtags)
        Connection.cursor.executescript(drop_tweets)
        Connection.cursor.executescript(drop_follows)
        Connection.cursor.executescript(drop_users)


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

        Connection.cursor.executescript(users_table)
        Connection.cursor.executescript(follows_table)
        Connection.cursor.executescript(tweets_table)
        Connection.cursor.executescript(hashtags_table)
        Connection.cursor.executescript(mentions_table)
        Connection.cursor.executescript(retweets_table)
        Connection.cursor.executescript(lists_table)
        Connection.cursor.executescript(includes_table)
        Connection.connection.commit()
