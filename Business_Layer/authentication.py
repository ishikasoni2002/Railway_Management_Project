from Business_Layer.admin_Users import AdminUsers as admin_users
import Database_Layer.db_utils as utils
from Database_Layer import connection
import bcrypt



class Authentication:

    # Initiating all tables
    def initiate_all_tables(self):
        utils.create_tables_if_not_exists()

    # Checking the root password
    def check_root_password(self, root_password):
        if root_password == 'Ishika@123':
            return True
        return False

    # LOGIN FUNCTIONS
    # Checking if role is admin or guest
    def check_if_admin_exists(self, username, password):
        username_and_password = utils.get_admin_details_from_username(username)
        if not username_and_password:
            return

        original_hashed_password = username_and_password[0][2]
        login_successful = bcrypt.checkpw(password.encode('utf-8'), original_hashed_password)
        if login_successful:
            return True
        else:
            return False

    def login_admin(self, username, password):
        is_admin_table_empty = utils.check_if_admin_table_empty()
        user_type = self.check_if_admin_exists(username, password)
        new_admin_user_object = admin_users()
        new_admin_user_object.insert_first_admin_into_AdminUsers(username, password)
        if user_type or is_admin_table_empty:
            return 'Admin'
        else:
            return 'Guest'


    def is_unique_username(self, username):
        all_usernames = utils.duplicate_usernames(username)
        if not all_usernames:
            return 1
        else:
            print('Username already exists!')
            return 0

    def signup_new_admin(self, username, password):
        utils.insert_new_admin(username, password)
