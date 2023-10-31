from Connection import Connection


class Setup:
    @staticmethod
    def drop_tables() -> None:
        """Runs a query to drop all existing tables in the db"""
        assert Connection.is_connected()

        dropQuery = """
        DROP TABLE IF EXISTS includes;
        DROP TABLE IF EXISTS lists;
        DROP TABLE IF EXISTS retweets;
        DROP TABLE IF EXISTS mentions;
        DROP TABLE IF EXISTS hashtags;
        DROP TABLE IF EXISTS tweets;
        DROP TABLE IF EXISTS follows;
        DROP TABLE IF EXISTS users;
        """
        Connection.cursor.executescript(dropQuery)


    def define_tables() -> None:
        """Runs a query to create new tables in db according to project spec"""
        assert Connection.is_connected()

        defineQuery = """
        CREATE TABLE users (
            usr         TEXT,
            pwd         TEXT,
            name        TEXT,
            email       TEXT,
            city        TEXT,
            timezone    REAL,
            PRIMARY KEY (usr)
        );
        CREATE TABLE follows (
            flwer       INTEGER,
            flwee       INTEGER,
            start_date  DATE,
            PRIMARY KEY (flwer, flwee),
            FOREIGN KEY (flwer) REFERENCES users(usr),
            FOREIGN KEY (flwee) REFERENCES users(usr)
        );
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
        CREATE TABLE hashtags (
            term        TEXT,
            PRIMARY KEY (term)
        );
        CREATE TABLE mentions (
            tid         INTEGER,
            term        TEXT,
            PRIMARY KEY (tid, term),
            FOREIGN KEY (tid) REFERENCES tweets(tid),
            FOREIGN KEY (term) REFERENCES hashtags(term)
        );
        CREATE TABLE retweets (
            usr         INTEGER,
            tid         INTEGER,
            rdate       DATE,
            PRIMARY KEY (usr, tid),
            FOREIGN KEY (usr) REFERENCES users(usr),
            FOREIGN KEY (tid) REFERENCES tweets(tid)
        );
        CREATE TABLE lists (
            lname       TEXT,
            owner       INTEGER,
            PRIMARY KEY (lname),
            FOREIGN KEY (owner) REFERENCES users(usr)
        );
        CREATE TABLE includes (
            lname       TEXT,
            member      INTEGER,
            PRIMARY KEY (lname, member),
            FOREIGN KEY (lname) REFERENCES lists(lname),
            FOREIGN KEY (member) REFERENCES users(usr)
        );
        """
        Connection.cursor.executescript(defineQuery)
        Connection.connection.commit()
