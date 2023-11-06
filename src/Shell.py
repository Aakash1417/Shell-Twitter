import os
from Connection import Connection
from Login import Login
from Search import Search
from ComposeTweet import ComposeTweet


class Shell:
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
    def get_main_options():
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
    def main_menu_do(cmd, additional_options=[]):
        """
            Presents a main menu with various options based on the user's login status

            Returns:
                A list of available menu options
        """
        options = Shell.get_main_options()
        if cmd in options:
            if cmd == "login":
                Login.login()
            elif cmd == "register":
                Login.register()
            elif cmd == "searchtweets":
                Search.search_for_tweets()
            elif cmd == "compose":
                ComposeTweet.createTweet()
            elif cmd == "searchusers":
                Search.search_for_users()
            elif cmd == "followers":
                pass
            elif cmd == "logout":
                pass
            elif cmd == "help":
                Shell.print_menu(additional_options)
            elif cmd == "exit":
                print("Closing Program :(")
                Connection.close()
                exit()
            elif cmd == "clear":
                Shell.clear()
        else:
            print("INVALID Command -_-")

    @staticmethod
    def print_menu(additional_options=[]):
        options = Shell.get_main_options()
        options = options[:-3] + additional_options + options[-3:]

        print("="*80)
        print()
        for option in options:
            print(f"- {option.capitalize()}")
        print()
        print("="*80)
        return options
