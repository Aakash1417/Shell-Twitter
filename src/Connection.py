import sqlite3

class Connection:
    connection = None
    cursor = None

    @staticmethod
    def is_connected():
        return Connection.connection is not None and Connection.cursor is not None


    @staticmethod
    def connect(path):
        Connection.connection = sqlite3.connect(path)
        Connection.cursor = Connection.connection.cursor()
        Connection.cursor.executescript(' PRAGMA foreign_keys=ON; ')
        Connection.connection.commit()
