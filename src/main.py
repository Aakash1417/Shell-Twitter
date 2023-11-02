import os
from Connection import Connection
from Setup import Setup
from Login import Login
from Shell import Shell
from Test import Test


def main():
    Shell.clear()
    path = os.path.dirname(os.path.realpath(__file__)) + "/data.db"
    Connection.connect(path)

    # Setup/dev methods
    Setup.drop_tables()
    Setup.define_tables()
    Test.insert_test_data()

    print("Welcome to crystal methadata!")

    while True:
        options = Shell.main_menu()
        cmd = input(">>> ").strip().lower()

        if cmd in options:
            if cmd == "login":
                Login.login()
            elif cmd == "register":
                Login.register()
            elif cmd == "searchtweets":
                pass
            elif cmd == "compose":
                pass
            elif cmd == "searchusers":
                pass
            elif cmd == "followers":
                pass
            elif cmd == "logout":
                pass
            elif cmd == "help":
                pass
            elif cmd == "exit":
                break
        elif cmd == "clear":
            Shell.clear()
        else:
            print("INVALID Command -_-")
            continue

    Connection.close()


if __name__ == "__main__":
    main()
