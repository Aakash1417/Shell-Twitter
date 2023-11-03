from Login import Login
from Connection import Connection
import datetime

class Follows():
    @staticmethod
    def follow(flwer:int) -> bool:
        query = "SELECT flwer FROM follows, users WHERE flwer = ? AND flwee = ?"
        if (Follows.contains(query, (Login.userID, flwer))):
            Connection.cursor.execute("SELECT name FROM users WHERE usr = ?", (flwer, ))
            result = Connection.cursor.fetchone()
            print("You already follow " + result[0])

        else:
            Connection.cursor.execute("INSERT INTO follows VALUES(?,?,?)", (Login.userID, flwer, datetime.date.today()))
            Connection.cursor.execute("SELECT name FROM users WHERE usr = ?", (flwer, ))
            result = Connection.cursor.fetchone()
            Connection.connection.commit()
            print("You started following " + result[0])
            
                   
    @staticmethod 
    def contains(query:str, values:tuple) -> bool:
        Connection.cursor.execute(query, values)
        result = Connection.cursor.fetchone()
        
        if result == None: return False
        else: return True