from getpass import getpass
import os
import string
import datetime

from Login import Login

from Setup import Setup
from Connection import Connection

class ComposeTweet:
    tweetNumber = 0
    def __init__(self) -> None:
        self.tweetNumber = self.countTweets()
              
    
    def countTweets(self):
        query = "SELECT tid FROM tweets"
        Connection.cursor.execute(query)
        
        all_entry = Connection.cursor.fetchall()
        
        if len(all_entry) == 0: return 0
        else: return max(all_entry[0])
        # for one_entry in all_entry:
    
    def createTweet(self, usr):
        tweet = input("Tweet message: ")
        self.findHashTags(tweet)
    

    def createTweetFromDB(self):
        query = "SELECT * FROM tweets;"
        Connection.cursor.execute(query)
        all_entry = Connection.cursor.fetchall()        
        for entry in all_entry:
            self.findHashTags(entry[0], entry[3])
        
        
    def findHashTags(self, tid:int, text:str):
        words = text.split()
        hashtags = []
        
        for word in words:
            if word[0].startswith("#"):
                for i in range(1, len(word)):
                    if word[i] in string.punctuation:
                        word = word[:i]
                        break
                hashtags.append(word[1:].lower())
        if len(hashtags) > 0:
            self.addHashtagsToMentions(tid, hashtags)
        
    
    def addHashtagsToMentions(self, tid:int, hashtags:list):
        for hashtag in hashtags:
            self.addHashtagsToHashtagsDB(hashtag)
            insert_query = 'INSERT INTO mentions (tid, term) VALUES (?, ?);'
            Connection.cursor.execute(insert_query, (tid, hashtag))
            self.addHashtagsToHashtagsDB(hashtag)
    
    def addHashtagsToHashtagsDB(self, hashtag:str):
        # Check if the hashtag exists in DB
        query = "SELECT term FROM hashtags WHERE term = ?;"
        Connection.cursor.execute(query, (hashtag,))
        result = Connection.cursor.fetchone()
        
        if result == None: #hashtag does not exist
            # insert hashtag to DB
            insert_query = "INSERT INTO hashtags (term) VALUES (?);"
            Connection.cursor.execute(insert_query, (hashtag,))
        
        Connection.connection.commit()

def SetUpTest():
    Setup.drop_tables()
    Setup.define_tables()
    Login.add_mock_users()
    
def AddTestTweets():
    # Connection.cursor.execute("PRAGMA foreign_keys = OFF;")
    # tweet_data = [(1, 1, '2023-10-27', 'This is a #test tweet.', 'Null'), (2,1, '2023-3-27', 'This is #another tweet that I am reply to someone else with', 1)]
    insert_query = f"""INSERT INTO tweets (tid, writer, tdate, text, replyto) VALUES 
                    (1, 1, 2023-10-27, 'This is a #test tweet.', NULL),
                    (2, 2, 2023-3-27, 'This is #another tweet that I am reply to someone else with', 1);"""
    Connection.cursor.executescript(insert_query)    
    Connection.connection.commit()
    # Connection.cursor.execute("PRAGMA foreign_keys = ON;")


if __name__ == "__main__":
    path = os.path.dirname(os.path.realpath(__file__)) + "/data.db"
    Connection.connect(path)
    ct = ComposeTweet()
    
    SetUpTest()
    AddTestTweets()
    
    ct.createTweetFromDB()