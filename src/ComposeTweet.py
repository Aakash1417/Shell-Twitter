import os
import string
import datetime

from Connection import Connection
from Login import Login
from Setup import Setup

class ComposeTweet:
    @staticmethod              
    def countTweets():
        """Counts the number of tweets and finds maximum tid

        Returns:
            int: maximum tid
        """
        query = "SELECT MAX(tid) FROM tweets"
        Connection.cursor.execute(query)
        entry = Connection.cursor.fetchone()
        
        if entry == None: return 0
        else: return entry[0]
    
    
    @staticmethod
    def createTweet(usr:int, replyTo:int = None):
        """The user wants to create a separate tweet or reply to a tweet and will prompt user for their message

        Args:
            replyTo (int, optional): the tweet that user is replying to. Defaults to None.
        """
        tweet = ""
        if replyTo == None: tweet = input("Enter tweet message: ")
        else: tweet = input("Enter reply to tweet "+ str(replyTo) + ": ")

        if tweet != "":
            tid = ComposeTweet.countTweets() + 1 # the tid for new tweet/reply
            ComposeTweet.addTweetToTweetsDB(tid, usr, tweet, replyTo)
            # ComposeTweet.findHashTags(tid,tweet)
        
    # @staticmethod
    # def processTweetFromDB():
    #     """_summary_
    #     """
    #     query = "SELECT * FROM tweets;"
    #     Connection.cursor.execute(query)
    #     all_entry = Connection.cursor.fetchall()        
    #     for entry in all_entry:
    #         ComposeTweet.findHashTags(entry[0], entry[3])
        
    @staticmethod
    def addTweetToTweetsDB(tid:int, user:int, tweet:str, replyTo:int):
        """it will add tweet to tweets table

        Args:
            tid (int): the tweet id
            user (int): the user id that writes the tweet
            tweet (str): the content of the tweet
            replyTo (int): the tid of tweet that the tweet is replying to (None if the tweet is not replying to another tweet)
        """
        insert_query = "INSERT INTO tweets (tid, writer, tdate, text, replyto) VALUES (?, ?, ?, ?, ?)"
        Connection.cursor.execute(insert_query, (tid, user, datetime.date.today(), tweet, replyTo))
        Connection.connection.commit()
        
        ComposeTweet.findHashTags(tid, tweet)
    
    
    @staticmethod    
    def findHashTags(tid:int, text:str):
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
    def addHashtagsToHashtagsDB(hashtag:str):
        """adds hashtag term to hashtags table

        Args:
            hashtag (str): the term
        """
        # Check if the hashtag exists in DB
        query = "SELECT term FROM hashtags WHERE term = ?;"
        containsDuplicate = ComposeTweet.checkForDuplicates(query, (hashtag,))
        
        if not containsDuplicate: #hashtag does not exist
            insert_query = "INSERT INTO hashtags (term) VALUES (?);"
            Connection.cursor.execute(insert_query, (hashtag,))
        
        Connection.connection.commit()
    
    
    @staticmethod
    def addHashtagsToMentionsDB(tid:int, hashtag:str):
        """adds hashtag term and the tweet id to mentions table

        Args:
            tid (int): the tweet id
            hashtag (str): the hashtag term found in the tweet
        """
        query = "SELECT tid,term FROM mentions WHERE tid = ? AND term = ?;"
        containsDuplicate = ComposeTweet.checkForDuplicates(query, (tid, hashtag))

        if not(containsDuplicate): # tweet doesn't contain the same hashtag
            insert_query = 'INSERT INTO mentions (tid, term) VALUES (?, ?);'
            Connection.cursor.execute(insert_query, (tid, hashtag))
            
        Connection.connection.commit()
        
        
    @staticmethod
    def checkForDuplicates(query:str, values:tuple) -> bool:
        """will find for duplicate items in database and return true if table contains values

        Args:
            query (str): given query
            values (tuple): values to look for in query

        Returns:
            bool: whether it contains an item with values given or not
        """
        Connection.cursor.execute(query, values)
        result = Connection.cursor.fetchone()
        
        if result == None: return False
        else: return True
        
    
def AddTestTweets():
    insert_query = f"""INSERT INTO tweets (tid, writer, tdate, text, replyto) VALUES 
                    (1, 1, 2023-10-27, 'This is a #test tweet.', NULL),
                    (2, 2, 2023-3-27, 'This is #another tweet that I am reply to someone else with', 1);"""
    Connection.cursor.executescript(insert_query)    
    Connection.connection.commit()
    
def test():
    Setup.drop_tables()
    Setup.define_tables()
    Login.add_mock_users()
    
    AddTestTweets()


if __name__ == "__main__":
    path = os.path.dirname(os.path.realpath(__file__)) + "/data.db"
    Connection.connect(path)

    test()
             
    usr = input("Username: ")
    code = input("tweet/reply?")
    
    if (code == "tweet"):
        ComposeTweet.createTweet(int(usr))
    else:
        replyTo = input("Replying to which tweet: ")
        ComposeTweet.createTweet(int(usr), int(replyTo))
    
