import os
from Connection import Connection
from Login import Login
from Search import Search


class Shell:
    current_state = None

    @staticmethod
    def clear():
        """
            Clears the screen
        """
        if os.name == 'posix':
            os.system('clear')
        elif os.name == 'nt':
            os.system('cls')

    @staticmethod
    def get_options():
        options = []
        if Login.userID is None:
            options.append("login")
            options.append("register")
        else:
            options.append("searchtweets")
            options.append("compose")
            options.append("searchusers")
            options.append("followers")
            options.append("logout")
        options.append("help")
        options.append("clear")
        options.append("exit")
        return options

    @staticmethod
    def main_menu_do(cmd):
        """
            Presents a main menu with various options based on the user's login status

            Returns:
                A list of available menu options
        """
        options = Shell.get_options()
        if cmd in options:
            if cmd == "login":
                Login.login()
            elif cmd == "register":
                Login.register()
            elif cmd == "searchtweets":
                Search.search_for_tweets()
            elif cmd == "compose":
                pass
            elif cmd == "searchusers":
                pass
            elif cmd == "followers":
                pass
            elif cmd == "logout":
                pass
            elif cmd == "help":
                Shell.print_menu()
            elif cmd == "exit":
                print("Closing Program :(")
                Connection.close()
                exit()
            elif cmd == "clear":
                Shell.clear()
        else:
            print("INVALID Command -_-")

    @staticmethod
    def print_menu():
        options = Shell.get_options()
        if Shell.current_state == 'viewTweet':
            options = options[:-3] + ["scrollup", "scrolldown",
                                      "reply", "retweet"] + options[-3:]

        print("="*32)
        print()
        for option in options:
            print(f"- {option.capitalize()}")
        print()
        print("="*32)
        return options
