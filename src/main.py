import os
from Connection import Connection
from Setup import Setup
from Login import Login


def main():
    path = os.path.dirname(os.path.realpath(__file__)) + "/data.db"
    Connection.connect(path)

    Setup.drop_tables()
    Setup.define_tables()

    Login.enter_user()
    user = Login.login()


if __name__ == "__main__":
    main()
