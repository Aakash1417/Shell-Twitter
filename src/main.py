import os
from Connection import Connection
from Setup import Setup
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
    Shell.print_menu()
    while True:
        cmd = input(">>> ").strip().lower()
        Shell.main_menu_do(cmd)


if __name__ == "__main__":
    main()
