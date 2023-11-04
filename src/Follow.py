from Login import Login
from Connection import Connection
import datetime


class Follow():
    @staticmethod
    def follow(flwer: int):
        """user logined in wants to follow the specified user id

        Args:
            flwer (int): the followers id
        """
        assert Connection.is_connected()
        query = "SELECT flwer FROM follows, users WHERE flwer = ? AND flwee = ?"
        if (Follow.contains(query, (Login.userID, flwer))):  # already follows the user
            print("You already follow " + Follow.getName(flwer))
        else:
            Connection.cursor.execute("INSERT INTO follows VALUES(?,?,?)",
                                      (Login.userID, flwer, datetime.date.today()))
            print("You started following " + Follow.getName(flwer))

    @staticmethod
    def contains(query: str, values: tuple) -> bool:
        """will find if table contains values

        Args:
            query (str): given query
            values (tuple): values to look for in query

        Returns:
            bool: whether it contains an item with values given
        """
        assert Connection.is_connected()
        Connection.cursor.execute(query, values)
        result = Connection.cursor.fetchone()

        if result == None:
            return False
        else:
            return True

    @staticmethod
    def getName(flwer: int) -> str:
        """gets the name of the user being followed

        Args:
            flwer (int): the follower to get the name of

        Returns:
            str: the name of the user
        """
        assert Connection.is_connected()
        Connection.cursor.execute("SELECT name FROM users WHERE usr = ?",
                                  (flwer, ))
        result = Connection.cursor.fetchone()
        Connection.connection.commit()
        return result[0]
