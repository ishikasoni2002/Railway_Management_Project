import unittest
from unittest.mock import patch
from Business_Layer.admin_Users import AdminUsers


class test_adminusers(unittest.TestCase):

#check_if_admin_exists
    @patch('Database_Layer.db_utils.get_admin_users',
           return_value=[('"Ishika123", "$2b$12$ZXonUdvRFCFkEZJeAEije.e4Z69y2EO53eV6piyUKP0xE2JvBtZtW"')])
    def test_check_if_admin_exists_success(self, mock_get_admin_users):
        adminObj = AdminUsers()
        count_admin = adminObj.check_if_admin_exists()
        mock_get_admin_users.assert_called_once()
        self.assertTrue(count_admin)

    @patch('Database_Layer.db_utils.get_admin_users', return_value=[])
    def test_check_if_admin_exists_failure(self, mock_get_admin_users):
        adminObj = AdminUsers()
        count_admin = adminObj.check_if_admin_exists()
        mock_get_admin_users.assert_called_once()
        self.assertFalse(count_admin)

#insert_first_admin_into_AdminUsers
    @patch('Business_Layer.admin_Users.utils.insert_first_admin_into_AdminUsers')
    @patch('Business_Layer.admin_Users.helper.generate_hash')
    @patch('Business_Layer.admin_Users.AdminUsers.check_if_admin_exists', return_value=False)
    def test_insert_first_admin_into_AdminUsers_success(self, mock_admin_exists, mock_generate_hash_pw,
                                                        mock_insert_first_admin):
        username = 'Ishika123'
        password = 'Ishika@123'

        adminObj = AdminUsers()
        hashed_password = 'abcde'
        mock_generate_hash_pw.return_value = hashed_password
        adminObj.insert_first_admin_into_AdminUsers(username, password)
        mock_admin_exists.assert_called_once()

        mock_generate_hash_pw.assert_called_once_with(password)
        mock_insert_first_admin.assert_called_once_with(username, hashed_password)

    @patch('Business_Layer.admin_Users.AdminUsers.check_if_admin_exists', return_value=True)
    def test_insert_first_admin_into_AdminUsers_Failure(self, mock_admin_exists):
        username = 'Ishika123'
        password = 'Ishika@123'

        adminObj = AdminUsers()

        adminObj.insert_first_admin_into_AdminUsers(username, password)
        mock_admin_exists.assert_called_once()



#insert_other_admin_into_AdminUsers
    @patch('Business_Layer.admin_Users.utils.insert_new_admin')
    @patch('Business_Layer.admin_Users.utils.get_admin_details_from_username')
    def test_insert_other_admin_into_AdminUsers_success(self, mock_get_admin_details, mock_insert_admin):
        username = 'Ishika123'
        password = 'Ishika@123'

        mock_get_admin_details.return_value = []

        adminObj = AdminUsers()
        adminObj.insert_other_admin_into_AdminUsers(username, password)

        mock_get_admin_details.assert_called_once_with(username)
        mock_insert_admin.assert_called_once_with(username, password)

    @patch('Business_Layer.admin_Users.utils.get_admin_details_from_username')
    def test_insert_other_admin_into_AdminUsers_Failure(self, mock_get_admin_details):
        username = 'Ishika123'
        password = 'Ishika@123'

        mock_get_admin_details.return_value = [('"Ishika123" ,"Ishkavhuui" ')]

        adminObj = AdminUsers()
        adminObj.insert_other_admin_into_AdminUsers(username, password)

        mock_get_admin_details.assert_called_once_with(username)