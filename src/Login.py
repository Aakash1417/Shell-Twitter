from getpass import getpass
from Connection import Connection


class Login:
    @staticmethod
    def enter_user():
        insert_user = '''
        INSERT INTO users(usr, pwd, name, email, city, timezone) VALUES
                                ('parshva', 'shah', 'Parshva Shah', 'p@gmailcom', 'Edmonton', 'MST');
        '''
        Connection.cursor.executescript(insert_user)
        Connection.connection.commit()

    @staticmethod
    def login():
        while (True):
            user = input("Enter your username (press 1 to create account): ")
            if user == "exit":
                exit()
            if user.isdigit():
                if int(user) == 1:
                    user = Login.register()
                    if user != None:
                        return user
            pswd = getpass('Enter your password:')
            if Login.userAuthentication(user, pswd):
                return user

    @staticmethod
    def register():
        pass

    @staticmethod
    def userAuthentication(username, password):
        data = (username, password)
        Connection.cursor.execute(
            f"SELECT pwd, name FROM users WHERE usr = '{username}';")

        # Fetch the result
        result = Connection.cursor.fetchone()

        if result is not None:  # The query returned a result

            # Assuming the password is in the first column (index 0)
            passwordSelected = result[0]

            if passwordSelected == password:
                print(result[1] + ", you have successfully logged in.")
                # Passwords match, authentication successful
                return username
            else:
                # Passwords don't match
                print("Incorrect password.")
                return None
        else:
            # No matching user found in the database
            print(username + " does not exist.")
            return None
