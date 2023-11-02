from getpass import getpass
from Connection import Connection


class Login:
    @staticmethod
    def add_mock_users() -> None:
        """Adds some mock users to the db for testing purposes"""
        assert Connection.is_connected()

        # hardcoded users
        insertQuery = """
        INSERT INTO users(usr, pwd, name, email, city, timezone) VALUES
                ('1', 'shah', 'Parshva Shah', 'p@gmailcom', 'Edmonton', '-7'),
                ('2', 'bruh', 'Tawfeeq Mannan', 'tawfeeq@gmail.com', 'Edmonton', '-7');
        """
        Connection.cursor.executescript(insertQuery)
        Connection.connection.commit()


    @staticmethod
    def get_highest_uid() -> int:
        """Finds the id of the user with the highest id

        Returns:
            int: highest user id in the db
        """
        assert Connection.is_connected()
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
            user = input("Enter your user id (alternatively, 'register' or 'exit'): ").strip()
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
        """Prompts user for information, then creates a new user in the db

        Returns:
            str: user id of the newly created user, or None on cancellation
        """
        assert Connection.is_connected()

        print("\nCreating new account.")
        print("You will be asked for a name, email, city, timezone, and password, " +
              "after which you can confirm your registration.\n")
        while (True):
            name = input("Display Name: ").strip()
            email = input("Email Address: ").strip()
            city = input("City: ").strip()
            timezone = input("Timezone (eg. -5): ").strip()
            password = getpass("Password: ")
            cPassword = getpass("Confirm Password: ")

            # pre-creation basic validation
            if '@' not in email or '.' not in email:  # very basic email validation
                print("\nEmail was an invalid format. Please try again.")
                continue
            try:
                timezone = float(timezone)
            except ValueError:
                print("\nTimezone must be a number. Please try again.")
                continue
            if password != cPassword:
                print("\nPasswords entered do not match. Please try again.")
                continue

            # confirm creation before committing
            confirmReg = input(f"\nCreate new account for {name}? (Y/n) ").strip()
            if not confirmReg.lower().startswith('y'):
                print("\nNew user registration cancelled. Returning to login prompt.")
                return None

            # create a new user with a unique uid
            uid = Login.get_highest_uid() + 1
            Connection.cursor.execute("""
            INSERT INTO users(usr, pwd, name, email, city, timezone) VALUES
                    (:usr, :pwd, :name, :email, :city, :timezone);
            """, {
                "usr": uid,
                "pwd": password,
                "name": name,
                "email": email,
                "city": city,
                "timezone": timezone
            })
            Connection.connection.commit()
            print(f"\nWelcome, {name}.")
            print(f"Your new user id is {uid}. You will need this id later to log in.\n")
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
            {"userid": userid}
        )
        result = Connection.cursor.fetchone()
        if result is None:
            print("No user with that id exists!")
            return False

        # otherwise, the query returned a result and the user exists
        # the correrct password is in the first column (index 0)
        correctPswd = result[0]
        if password == correctPswd:
            # authentication successful
            print(f"Welcome back, {result[1]}.\n")
            return True
        else:
            # Passwords don't match
            print("Incorrect password.")
            return False
