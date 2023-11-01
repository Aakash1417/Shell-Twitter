from getpass import getpass
import string
from Connection import Connection

class ComposeTweet:
    tweetNumber = 0
    def __init__(self) -> None:
        self.tweetNumber = self.countTweets()
        
        
    def countTweets(self):
        query = "SELECT tid FROM tweets"
        Connection.cursor.execute(query)
        
        all_entry = Connection.cursor.fetchall()
        
        if len(all_entry == 0): return 0
        else: return max(all_entry[0])
        # for one_entry in all_entry:
    
    def createTweet(self, usr):
        tweet = input("Tweet message: ")
        self.findHashTags(tweet)
        
    def findHashTags(self, text:str):
        words = text.split()
        hashtag = []
        
        j = 0
        for word in words:
            if word[0].startswith("#"):
                for i in range(1, len(word)):
                    if word[i] in string.punctuation:
                        word = word[:i]
                        break
                    hashtag.append(word[1:].lower())
        if len(hashtag) > 0: self.addHashtagsToDB(hashtag)
        
    def addHashtagsToDB(hashtags:list):
        
        for hashtag in hashtags:
            # Check if the hashtag exists in the database
            query = "SELECT term FROM hashtags WHERE hashtag = %s"
            Connection.cursor.execute(query, (hashtag,))
            result = Connection.cursor.fetchone()
            
            if result == None:
                # Hashtag doesn't exist; insert it
                insert_query = "INSERT INTO hashtags (hashtag) VALUES (%s)"
                Connection.cursor.execute(insert_query, (hashtag,))
        
        Connection.cursor.execute()
        Connection.connection.commit()
    
if __name__ == "__main__":
    ComposeTweet.createTweet("hello")