import Database_Layer.db_utils as utils
import Business_Layer.helper as helper


class AdminUsers:


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



