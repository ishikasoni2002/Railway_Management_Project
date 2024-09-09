import unittest
from unittest.mock import patch
from Business_Layer.admin_Users import AdminUsers
import Database_Layer.db_utils as utils

class test_adminusers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.admin_users_obj = AdminUsers()
    @patch('Database_Layer.db_utils.get_admin_details_from_username', return_value=True)
    def test_create_new_admin_username_present(self, mocked_get_admin_details):
        admin_obj = AdminUsers()
        result = admin_obj.create_new_admin('Ishika123', 'Ishika@123')
        assert result == 0
        mocked_get_admin_details.assert_called_once_with('Ishika123')

    @patch('Database_Layer.db_utils.insert_new_admin', return_value=None)
    @patch('Business_Layer.helper.generate_hash', return_value=b'Password')
    @patch('Database_Layer.db_utils.get_admin_details_from_username', return_value=False)
    def test_create_new_admin_username_not_present(self, mocked_get_admin_details, mocked_generate_hash,
                                              mocked_insert_new_admin):
        result = self.admin_users_obj.create_new_admin('Ishika123', 'Ishika@123')
        mocked_get_admin_details.assert_called_once_with('Ishika123')
        mocked_generate_hash.assert_called_once_with('Ishika@123')
        mocked_insert_new_admin.assert_called_once_with('Ishika123', b'Password')
        assert result == 1

    def test_set_username(self):
        self.admin_users_obj.set_username('Ishika')
        assert self.admin_users_obj.username == 'Ishika'

    def test_get_username(self):
        result = self.admin_users_obj.get_username()
        assert result == {'username': self.admin_users_obj.username}

    @patch('Database_Layer.db_utils.get_admin_details_from_username')
    def test_remove_admin_not_existing(self,mocked_get_admin_details):
        mocked_get_admin_details.return_value = False
        self.admin_users_obj.remove_an_admin('Ishika234')
        mocked_get_admin_details.assert_called_once_with('Ishika234')

    @patch('Database_Layer.db_utils.delete_admin')
    @patch('Database_Layer.db_utils.get_admin_details_from_username')
    def test_remove_admin_existing_self_delete(self, mocked_get_admin_details,mocked_delete_admin):
        self.admin_users_obj.username = 'Ishika'
        mocked_get_admin_details.return_value = [['name','Ishika']]
        mocked_delete_admin.return_value = None
        print(self.admin_users_obj.username)
        self.admin_users_obj.remove_an_admin('Ishika')
        mocked_get_admin_details.assert_called_once_with('Ishika')

    @patch('Database_Layer.db_utils.delete_admin')
    @patch('Database_Layer.db_utils.get_admin_details_from_username')
    def test_remove_admin_existing_others_delete(self, mocked_get_admin_details, mocked_delete_admin):
        mocked_get_admin_details.return_value = [['name', 'Aman']]
        self.admin_users_obj.username = 'Anand'
        mocked_delete_admin.return_value = None
        print(self.admin_users_obj.username)
        self.admin_users_obj.remove_an_admin('Aman')
        mocked_get_admin_details.assert_called_once_with('Aman')
        mocked_delete_admin.assert_called_once_with('Aman')

    # check_if_admin_exists
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

    # insert_first_admin_into_AdminUsers
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

    # insert_other_admin_into_AdminUsers
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

