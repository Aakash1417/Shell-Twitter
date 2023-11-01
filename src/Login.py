from getpass import getpass
from hashlib import sha256
from Connection import Connection


class Login:
    @staticmethod
    def add_mock_users() -> None:
        """Adds some mock users to the db for testing purposes"""
        assert Connection.is_connected()

        # hardcoded users. it's ok to use string formatting here, since no user input
        hashes = [Login.hashPswd("shah", "1"), Login.hashPswd("bruh", "2")]
        insertQuery = f"""
        INSERT INTO users(usr, pwd, name, email, city, timezone) VALUES
                ('1', '{hashes[0]}', 'Parshva Shah', 'p@gmailcom', 'Edmonton', '-7'),
                ('2', '{hashes[1]}', 'Tawfeeq Mannan', 'tawfeeq@gmail.com', 'Edmonton', '-7');
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
    def get_highest_uid() -> int:
        """Finds the id of the user with the highest id

        Returns:
            int: highest user id in the db
        """
        Connection.cursor.execute("SELECT MAX(usr) FROM users;")
        result = Connection.cursor.fetchone()
        if result is None:
            return 0
        return int(result[0])


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
    def register() -> str:
        assert Connection.is_connected()

        print("Creating new account.")
        print("You will be asked for a name, email, city, timezone, and password, " +
              "after which you can confirm your registration.")
        while (True):
            name = input("Display Name: ")
            email = input("Email Address: ")
            city = input("City: ")
            timezone = input("Timezone (eg. -5): ")
            password = getpass("Password: ")
            cPassword = getpass("Confirm Password: ")

            # pre-creation basic validation
            if '@' not in email or '.' not in email:  # very basic check
                print("\nEmail was an invalid format. Please try again.")
                continue
            try:
                timezone = float(timezone)
            except ValueError:
                print("\nTimezone must be a floating-point number. Please try again.")
                continue
            if password != cPassword:
                print("\nPasswords entered do not match. Please try again.")
                continue

            # confirm creation before committing
            confirmReg = input(f"\nCreate new account for {name}? (Y/n) ")
            if not confirmReg.lower().startswith('y'):
                print("\nNew user registration cancelled. Returning to login prompt.")
                return None

            # create a new user with a unique uid
            uid = Login.get_highest_uid() + 1
            pwd = Login.hashPswd(password, str(uid))
            Connection.cursor.execute("""
            INSERT INTO users(usr, pwd, name, email, city, timezone) VALUES
                    (:usr, :pwd, :name, :email, :city, :timezone);
            """, {
                "usr": uid,
                "pwd": pwd,
                "name": name,
                "email": email,
                "city": city,
                "timezone": timezone
            })
            Connection.connection.commit()
            print(f"Welcome, {name}.")
            print(f"Your new user id is {uid}. You will need this id to log in.\n")
            return str(uid)


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
        if Login.hashPswd(password, str(userid)) == correctPswd:
            # authentication successful
            print(f"Welcome back, {result[1]}.\n")
            return True
        else:
            # Passwords don't match
            print("Incorrect password.")
            return False
