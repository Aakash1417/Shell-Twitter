import os

from Login import Login
from Test import Test
from Setup import Setup
from Connection import Connection
from ComposeTweet import ComposeTweet

class Followers:
    followersList = []
    follower = 0
    followerTweetList = []
    followersCount = 0
    currentFirstTweet = 0
    currentLastTweet = 3
        

    def getFollowers(self):
        query = "SELECT usr, name, city FROM follows, users WHERE flwee = ? AND flwer = usr ORDER BY start_date DESC"
        Connection.cursor.execute(query, (Login.userID,))
        
        result = Connection.cursor.fetchall()
        print("="*32)
        for values in result:
            self.followersCount+=1
            print(str(self.followersCount) + "]")
            print("\t" + str(values[0]) + "\n\t" + values[1] + " \n\t" + values[2])
            print("="*32)
        self.followersList = result
        self.takeInput()


    def takeInput(self):
        followerSelected = False
        while True:
            cmd = input(">>> ").strip().split()
            if cmd[0] == "select" and cmd[1].isnumeric() and len(cmd) == 2:
                if int(cmd[1]) > self.followersCount or int(cmd[1]) < 1: print("Follower not in list.")
                else: 
                    self.follower = self.followersList[int(cmd[1])-1][0]
                    tweetCount, followers, followees = self.getFollowerInfo()
                    print("Tweet Count: {}\t Followers: {} \t Following: {}".format(tweetCount, followers, followees))
                    self.getFollowerTweets()
                    print("="*32)
                    self.displayTweets()
                    followerSelected = True
            elif cmd[0] == "scroll" and cmd[1] == "down" and len(cmd) == 2 and followerSelected == True:
                if self.currentLastTweet != len(self.followerTweetList):
                    self.currentFirstTweet = min(self.currentLastTweet, len(self.followerTweetList))
                    if self.currentLastTweet + 3 > len(self.followerTweetList):
                        self.currentLastTweet = len(self.followerTweetList)
                    else: self.currentLastTweet += 3
                self.displayTweets()
                
            elif cmd[0] == "scroll" and cmd[1] == "up" and len(cmd) == 2 and followerSelected == True:
                if self.currentFirstTweet != 0:
                    self.currentLastTweet = max(self.currentFirstTweet, 0)
                    if self.currentFirstTweet - 3 < 0:
                        self.currentLastTweet = 0
                    else: self.currentFirstTweet -= 3
                self.displayTweets()
                
            elif cmd[0] == "reply" and cmd[1].isnumeric() and len(cmd) == 2 and followerSelected == True:
                if int(cmd[1]) > len(self.followerTweetList) or int(cmd[1]) < 1: print("Invalid tweet selected.")
                else:
                    ComposeTweet.createTweet(self.followerTweetList[int(cmd[1])-1][0])
                
                
                    

    
    def getFollowerInfo(self):
        tweets = self.getNumberOfTweets()
        followers = self.getNumberOfFollowers()
        followees = self.getNumberOfFollowing()
        return tweets, followers, followees
        
    
    def getNumberOfTweets(self):
        query = "SELECT COUNT(*) FROM tweets WHERE writer = ?"
        Connection.cursor.execute(query, (self.follower,))
        
        result = Connection.cursor.fetchone()
        if result == None: return 0
        else: return result[0]
   
    
    def getNumberOfFollowers(self):
        query = "SELECT COUNT(*) FROM follows WHERE flwee = ?"
        Connection.cursor.execute(query, (self.follower,))
        
        result = Connection.cursor.fetchone()
        if result == None: return 0
        else: return result[0]
    
    
    def getNumberOfFollowing(self):
        query = "SELECT COUNT(*) FROM follows WHERE flwer = ?"
        Connection.cursor.execute(query, (self.follower,))
        
        result = Connection.cursor.fetchone()
        if result == None: return 0
        else: return result[0]
   
        
    def getFollowerTweets(self):
        query = "SELECT tid, text, tdate FROM tweets WHERE writer = ? ORDER BY tdate DESC"
        Connection.cursor.execute(query, (self.follower,))
        
        result = Connection.cursor.fetchall()
        self.followerTweetList = result
    
        
    def displayTweets(self):        
        if not(self.currentFirstTweet >= self.currentLastTweet):
            for i in range(self.currentFirstTweet, self.currentLastTweet):
                print("{}]".format(i+1))
                print(self.followerTweetList[i][1])
                print("Date posted: {}".format(self.followerTweetList[i][2]))
                print("="*32)
            

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
    
    userInfo = Followers()
    followers = userInfo.getFollowers() 
    