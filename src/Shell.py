import os
from Login import Login


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
    def main_menu():
        """
            Presents a main menu with various options based on the user's login status

            Returns:
                A list of available menu options
        """
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
        options.append("exit")

        print("="*32)
        print()
        for option in options:
            print(f"- {option.capitalize()}")
        print()
        print("="*32)
        return options
