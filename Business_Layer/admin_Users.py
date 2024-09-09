import Database_Layer.db_utils as utils
import Business_Layer.helper as helper


class AdminUsers:

    def __init__(self):
        self.username = None
        self.password = None


    def create_new_admin(self,username, password):
        username_already_present = utils.get_admin_details_from_username(username)
        if not username_already_present:
            hashed_password = helper.generate_hash(password)
            utils.insert_new_admin(username, hashed_password)
            return 1
        else:
            return 0

    def set_username(self, username):
        self.username = username

    def get_username(self):
        return {'username': self.username}

    def remove_an_admin(self,username):
        is_admin_existing = utils.get_admin_details_from_username(username)
        if is_admin_existing:
            if self.username != is_admin_existing[0][1]:
                utils.delete_admin(username)
                print(f'{username} has been deleted! ')
            else:
                print('You cannot delete yourself! ')
        else:
            print('No such admin exists! ')





    def check_if_admin_exists(self):
        count_of_admins = utils.get_admin_users()
        if count_of_admins:
            return True
        else:
            return False

    def insert_first_admin_into_AdminUsers(self, username, password):
        list_of_admins = self.check_if_admin_exists()
        username = 'Ishika123'
        password = 'Ishika@123'

        if not list_of_admins:
            hashed_password = helper.generate_hash(password)
            utils.insert_first_admin_into_AdminUsers(username, hashed_password)

    def insert_other_admin_into_AdminUsers(self, username, password):
        admin_details = utils.get_admin_details_from_username(username)
        if admin_details:
            print('Username Already Exists!')
        else:
            utils.insert_new_admin(username, password)



