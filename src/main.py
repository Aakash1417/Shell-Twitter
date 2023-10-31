import sqlite3
import os
from Setup import Setup
from Login import Login


def main():
    path = os.path.dirname(os.path.realpath(__file__)) + "/data.db"
    Setup.connect(path)
    Setup.drop_tables()
    Setup.define_tables()

    Login.set_connection(Setup.connection, Setup.cursor)
    Login.enter_user()
    user = Login.login()


if __name__ == "__main__":
    main()
