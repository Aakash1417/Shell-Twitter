import os

from Login import Login
from Test import Test
from Setup import Setup
from Connection import Connection
from ComposeTweet import ComposeTweet
from Follow import Follow


class Followers:
    followersList = []
    follower = 0
    followerTweetList = []
    followersCount = 0
    currentFirstTweet = 0
    currentLastTweet = 3

    def __init__(self) -> None:
        self.followersList = []
        self.follower = 0
        self.followerTweetList = []
        self.followersCount = 0
        self.currentFirstTweet = 0
        self.currentLastTweet = 3

    def getFollowers(self) -> str:
        """ prints out all the users of the logged in user

        Returns:
            str: returns a global command once user is done with using followers page
        """
        assert Connection.is_connected()
        query = "SELECT usr, name, city FROM follows, users WHERE flwee = ? AND flwer = usr ORDER BY start_date DESC"
        Connection.cursor.execute(query, (Login.userID,))

        result = Connection.cursor.fetchall()
        print("="*32)
        for values in result:
            self.followersCount += 1
            print(str(self.followersCount) + "]")
            print("\t" + str(values[0]) + "\n\t" +
                  values[1] + " \n\t" + values[2])
            print("="*32)
        self.followersList = result
        globalCmd = self.takeInput()
        # TODO: use global command as input for Shell class
        return globalCmd

    def takeInput(self) -> str:
        """takes input for what user wants to do with followers page

        Returns:
            str: global command (leave followers page)
        """
        # flag for when follower is selected as only some actions can be done after follower selected
        followerSelected = False
        while True:
            cmd = input(">>> ").strip().split()
            if cmd[0] == "select" and cmd[1].isnumeric() and len(cmd) == 2:
                if int(cmd[1]) > self.followersCount or int(cmd[1]) < 1:
                    print("Follower not in list.")
                else:
                    self.getFollowerInfo(int(cmd[1])-1)
                    followerSelected = True
            elif cmd[0] == "scroll" and cmd[1] == "down" and len(cmd) == 2 and followerSelected:
                self.scrollDown()
            elif cmd[0] == "scroll" and cmd[1] == "up" and len(cmd) == 2 and followerSelected:
                self.scrollUp()
            elif cmd[0] == "reply" and cmd[1].isnumeric() and len(cmd) == 2 and followerSelected:
                if int(cmd[1]) > len(self.followerTweetList) or int(cmd[1]) < 1:
                    print("Invalid tweet selected.")
                else:
                    ComposeTweet.createTweet(
                        self.followerTweetList[int(cmd[1])-1][0])
            elif cmd[0] == "retweet" and cmd[1].isnumeric() and len(cmd) == 2 and followerSelected:
                if int(cmd[1]) > len(self.followerTweetList) or int(cmd[1]) < 1:
                    print("Invalid tweet selected.")
                else:
                    ComposeTweet.createRetweet(
                        self.followerTweetList[int(cmd[1])-1][0])
            elif cmd[0] == "follow" and len(cmd) == 1 and followerSelected:
                Follow.follow(self.follower)
            elif cmd[0] == "follow" and len(cmd) == 1 and not followerSelected:
                print("You must select a follower from the list.")
            # FIXME: check cmd for if it is in the global command list
            elif cmd[0] == "exit" and len(cmd) == 1:
                return cmd[0]
            else:
                print("Invalid Command")

    def getFollowerInfo(self, flwer: int) -> None:
        """_summary_

        Args:
            flwer (int): _description_
        """
        self.follower = self.followersList[flwer][0]
        # gets follower information
        tweets = self.getNumberOfTweets()
        followers = self.getNumberOfFollowers()
        followees = self.getNumberOfFollowing()

        # prints selected followers details
        print("\nYou are looking at " +
              Follow.getName(self.follower) + "'s profile.")
        print("Tweet Count: {}\t Followers: {} \t Following: {}".format(
            tweets, followers, followees))
        self.getFollowerTweets()
        print("="*32)
        self.currentFirstTweet = 0
        self.currentLastTweet = min(3, len(self.followerTweetList))
        if self.currentLastTweet == 0:
            print("User has not posted any tweets.")
            print("="*32)
        else:
            self.scrollUp()

    def getNumberOfTweets(self) -> int:
        """gets the number of tweets that selected followers has posted/retweeted

        Returns:
            int: number of tweets
        """
        assert Connection.is_connected()

        # number of tweets
        query = "SELECT COUNT(*) FROM tweets WHERE writer = ?"
        Connection.cursor.execute(query, (self.follower,))
        tweetResult = Connection.cursor.fetchone()

        # number of retweets
        query = "SELECT COUNT(*) FROM retweets WHERE usr = ?"
        Connection.cursor.execute(query, (self.follower,))
        retweetResult = Connection.cursor.fetchone()

        if tweetResult == None:
            tweetResult[0] = 0
        if retweetResult == None:
            retweetResult[0] = 0
        return (tweetResult[0] + retweetResult[0])

    def getNumberOfFollowers(self) -> int:
        """returns the number of followers of the selected follower

        Returns:
            int: number of followers
        """
        assert Connection.is_connected()
        query = "SELECT COUNT(*) FROM follows WHERE flwee = ?"
        Connection.cursor.execute(query, (self.follower,))

        result = Connection.cursor.fetchone()
        if result == None:
            return 0
        else:
            return result[0]

    def getNumberOfFollowing(self) -> int:
        """returns the number of user following selected follower

        Returns:
            int: number of users following
        """
        assert Connection.is_connected()
        query = "SELECT COUNT(*) FROM follows WHERE flwer = ?"
        Connection.cursor.execute(query, (self.follower,))

        result = Connection.cursor.fetchone()
        if result == None:
            return 0
        else:
            return result[0]

    def getFollowerTweets(self) -> None:
        """gets tweets and retweets of selected follower
        """
        assert Connection.is_connected()
        query = "SELECT tid, text, tdate FROM tweets WHERE writer = ? UNION SELECT r.tid, t.text, r.rdate FROM retweets r, tweets t WHERE t.tid = r.tid AND r.usr = ? ORDER BY tdate DESC"
        Connection.cursor.execute(query, (self.follower, self.follower))

        result = Connection.cursor.fetchall()
        self.followerTweetList = result

    def scrollDown(self) -> None:
        """scrolls down to view next three tweets
        """
        if self.currentLastTweet != len(self.followerTweetList):
            self.currentFirstTweet = min(
                self.currentLastTweet, len(self.followerTweetList))
            if self.currentLastTweet + 3 > len(self.followerTweetList):
                self.currentLastTweet = len(self.followerTweetList)
            else:
                self.currentLastTweet += 3
        self.displayTweets()

    def scrollUp(self) -> None:
        """scrolls up to view previous three tweets
        """
        if self.currentFirstTweet != 0:
            self.currentLastTweet = max(self.currentFirstTweet, 0)
            if self.currentFirstTweet - 3 < 0:
                self.currentLastTweet = 0
            else:
                self.currentFirstTweet -= 3
        self.displayTweets()

    def displayTweets(self) -> None:
        """displays the tweets (3 at a time)
        """
        if not (self.currentFirstTweet >= self.currentLastTweet):
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
