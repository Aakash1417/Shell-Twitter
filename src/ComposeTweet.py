import os
import string
import datetime

from Connection import Connection
from Login import Login
from Test import Test
from Setup import Setup

class ComposeTweet:
    @staticmethod              
    def countTweets() -> int:
        """Counts the number of tweets and finds maximum tid

        Returns:
            int: maximum tid
        """
        assert Connection.is_connected()
        query = "SELECT MAX(tid) FROM tweets"
        Connection.cursor.execute(query)
        entry = Connection.cursor.fetchone()
        
        if entry == None: return 0
        else: return entry[0]
    
    
    @staticmethod
    def createTweet(replyTo:int = None) -> None:
        """The user wants to create a separate tweet or reply to a tweet and will prompt user for their message

        Args:
            replyTo (int, optional): the tweet that user is replying to. Defaults to None.
        """
        tweet = ""
        # checks if it is a tweet or reply (checks if tweet being replied to exists)
        if replyTo == None: tweet = input("Enter tweet message: ")
        elif ComposeTweet.contains("SELECT tid FROM tweets WHERE tid = ?;", (replyTo,)): 
            tweet = input("Enter reply: ")
        else:
            print("Tweet does not exist.")
        

        if tweet != "":
            tid = ComposeTweet.countTweets() + 1 # the tid for new tweet/reply
            ComposeTweet.addTweetToTweetsDB(tid, tweet, replyTo)


    @staticmethod
    def createRetweet(tid:int) -> None:
        if ComposeTweet.contains("SELECT tid FROM retweets WHERE tid = ? AND usr = ?;", (tid, Login.userID)): 
            print("You have already retweeted this tweet.")
        else:
            ComposeTweet.addRetweetToDB(tid)
        
        
    @staticmethod
    def addTweetToTweetsDB(tid:int, tweet:str, replyTo:int) -> None:
        """it will add tweet to tweets table

        Args:
            tid (int): the tweet id
            tweet (str): the content of the tweet
            replyTo (int): the tid of tweet that the tweet is replying to (None if the tweet is not replying to another tweet)
        """
        assert Connection.is_connected()
        insert_query = "INSERT INTO tweets (tid, writer, tdate, text, replyto) VALUES (?, ?, ?, ?, ?)"
        Connection.cursor.execute(insert_query, (tid, Login.userID, datetime.date.today(), tweet, replyTo))
        Connection.connection.commit()
        
        if replyTo == None: print("Your tweet has successfully been posted!")
        else: print("Your reply has successfully been posted!")
        
        ComposeTweet.findHashTags(tid, tweet)
    
    
    @staticmethod    
    def findHashTags(tid:int, text:str) -> None:
        """Finds all the hashtags in the message

        Args:
            tid (int): the tweet id
            text (str): the text that is checked for any hashtags
        """
        words = text.split()
        hashtags = []
        
        for word in words:
            if word[0].startswith("#"):
                for i in range(1, len(word)):
                    # will process characters after '#' before any punctuations
                    # assumptions is that hashtags are alphanumeric
                    if word[i] in string.punctuation:
                        word = word[:i]
                        break
                hashtags.append(word[1:].lower())
        if len(hashtags) > 0:
            for hashtag in hashtags:
                ComposeTweet.addHashtagsToHashtagsDB(hashtag)
                ComposeTweet.addHashtagsToMentionsDB(tid, hashtag)
        
    
    @staticmethod
    def addHashtagsToHashtagsDB(hashtag:str) -> None:
        """adds hashtag term to hashtags table

        Args:
            hashtag (str): the term
        """
        assert Connection.is_connected()
        # Check if the hashtag exists in DB
        query = "SELECT term FROM hashtags WHERE term = ?;"
        containsDuplicate = ComposeTweet.contains(query, (hashtag,))
        
        if not containsDuplicate: #hashtag does not exist
            insert_query = "INSERT INTO hashtags (term) VALUES (?);"
            Connection.cursor.execute(insert_query, (hashtag,))
        
        Connection.connection.commit()
    
    
    @staticmethod
    def addHashtagsToMentionsDB(tid:int, hashtag:str) -> None:
        """adds hashtag term and the tweet id to mentions table

        Args:
            tid (int): the tweet id
            hashtag (str): the hashtag term found in the tweet
        """
        assert Connection.is_connected()
        query = "SELECT tid,term FROM mentions WHERE tid = ? AND term = ?;"
        containsDuplicate = ComposeTweet.contains(query, (tid, hashtag))

        if not(containsDuplicate): # tweet doesn't contain the same hashtag
            insert_query = 'INSERT INTO mentions (tid, term) VALUES (?, ?);'
            Connection.cursor.execute(insert_query, (tid, hashtag))
            
        Connection.connection.commit()
    
    
    @staticmethod
    def addRetweetToDB(tid:int):
        assert Connection.is_connected()
        insert_query = "INSERT INTO retweets (usr, tid, rdate) VALUES (?, ?, ?)"
        Connection.cursor.execute(insert_query, (Login.userID, tid, datetime.date.today()))
        Connection.connection.commit()
        
        print("Your retweet has successfully been posted! ")
    
        
    @staticmethod
    def contains(query:str, values:tuple) -> bool:
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
        
        if result == None: return False
        else: return True
        
def test() -> None:
    """Creates test tables
    """
    path = os.path.dirname(os.path.realpath(__file__)) + "/data.db"
    Connection.connect(path)
    Setup.drop_tables()
    Setup.define_tables()
    Test.insert_test_data()

if __name__ == "__main__":
    
    test()
    
    # manually enter User ID
    usr = input("User ID: ")
    Login.userID = int(usr)

    while(True):
        code = input("tweet/reply <tid>?")
        inputs = code.split()
        if (inputs[0] == "tweet" and len(inputs) == 1):
            ComposeTweet.createTweet()
        elif (inputs[0] == "reply" and inputs[1].isnumeric() and len(inputs) == 2):
            ComposeTweet.createTweet(int(inputs[1]))
        elif (inputs[0] == "exit"): break
        else: print("Invalid command.")
        
        Connection.close()
