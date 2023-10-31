import sqlite3


class Connection:
    connection = None
    cursor = None

    @staticmethod
    def is_connected() -> bool:
        """Determines whether the connection has been established

        Returns:
            bool: True if db has successfully connected
        """
        return Connection.connection is not None and Connection.cursor is not None


    @staticmethod
    def connect(path: str) -> None:
        """Initializes the db connection

        Args:
            path (str): filepath to the db to connect to
        """
        Connection.connection = sqlite3.connect(path)
        Connection.cursor = Connection.connection.cursor()
        Connection.cursor.executescript(' PRAGMA foreign_keys=ON; ')
        Connection.connection.commit()
