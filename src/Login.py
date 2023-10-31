from getpass import getpass
from hashlib import sha256
from Connection import Connection


class Login:
    @staticmethod
    def add_mock_users() -> None:
        """Adds some mock users to the db for testing purposes"""
        assert Connection.is_connected()

        insertQuery = """
        INSERT INTO users(usr, pwd, name, email, city, timezone) VALUES
                                ('1', 'shah', 'Parshva Shah', 'p@gmailcom', 'Edmonton', '-7'),
                                ('2', 'bruh', 'Tawfeeq Mannan', 'tawfeeq@gmail.com', 'Edmonton', '-7');
        """
        Connection.cursor.executescript(insertQuery)
        Connection.connection.commit()


    @staticmethod
    def hashPswd(pswd: str, salt: str=None) -> str:
        """Generates the hashed version of a password, with optional salt

        Args:
            pswd (str): password to hash
            salt (str, optional): salt to include before hashing. Defaults to None.

        Returns:
            str: hashed version of password
        """
        alg = sha256()
        if salt is not None:
            pswd += salt
        alg.update(pswd.encode("utf-8"))
        return alg.hexdigest()


    @staticmethod
    def login() -> str:
        """Runs the login service until a user successfully authenticates, or exits

        Returns:
            str: on successful authentication, the user's id. otherwise 'exit'
        """
        while (True):
            user = input("Enter your user id (alternatively, 'register' or 'exit'): ")
            if user.lower() == "exit":
                return "exit"

            if user.lower() == "register":
                user = Login.register()
                if user is not None:  # new user registered successfully
                    return user
                else:  # registration cancelled
                    continue

            if not user.isnumeric():
                print("User id must be numeric.")
                continue

            uid = int(user)
            pswd = getpass("Enter your password: ")
            if Login.authenticate_user(uid, pswd):
                return user


    @staticmethod
    def register():
        pass


    @staticmethod
    def authenticate_user(userid: int, password: str) -> bool:
        """Authenticates a user's login credentials

        Args:
            userid (int): id of the user attempting to login
            password (str): attempted password (unhashed)

        Returns:
            bool: True if the user login credentials are valid
        """
        assert Connection.is_connected()

        # check if the user exists
        Connection.cursor.execute(
            "SELECT pwd, name FROM users WHERE usr = :userid;",
            {"userid": userid})
        result = Connection.cursor.fetchone()
        if result is None:
            print("No user with that id exists!")
            return False

        # otherwise, the query returned a result and the user exists
        # the correrct password is in the first column (index 0)
        correctPswd = result[0]
        if password == correctPswd:
            # authentication successful
            print(f"Welcome back, {result[1]}.")
            return True
        else:
            # Passwords don't match
            print("Incorrect password.")
            return False
