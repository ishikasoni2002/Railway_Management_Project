import unittest
from unittest.mock import patch
from Business_Layer.authentication import Authentication


class TestAuthentication(unittest.TestCase):

    # @patch('test_authentication.Authentication')
    # @patch('test_authentication.create_tables_if_not_exists')
    # def test_initiate_all_tables(self, mock_create_tables, mock_auth):
    #     mock_auth.
    #     auth.initiate_all_tables()
    #     mock_create_tables.assert_called_once()

    @patch('Database_Layer.db_utils.create_tables_if_not_exists')
    def test_initiate_all_tables(self, mock_create_tables):
        auth = Authentication()
        auth.initiate_all_tables()
        mock_create_tables.assert_called_once()

    def test_check_root_password(self):
        auth = Authentication()
        self.assertFalse(auth.check_root_password('Ishika23'), 'Ishika@123')
        self.assertTrue(auth.check_root_password('Ishika@123'), 'Ishika@123')

    # @patch('Database_Layer.db_utils.get_hashed_password')
    # @patch('bcrypt.checkpw')
    # def test_is_admin_success(self, mock_checkpw, mock_get_hashed_password):
    #     auth = Authentication()
    #     mock_get_hashed_password.return_value = b'$2b$12$eix6Mh.6.O1M4fTzT5O1heQ6V.b0U8z6WnR8qxK8B/ywWjRvvMyQK'  # Example hashed password
    #     mock_checkpw.return_value = True
    #
    #     result = auth.is_admin('testuser', 'correctpassword')
    #
    #     self.assertTrue(result)

    @patch('Business_Layer.authentication.utils.get_admin_details_from_username')
    @patch('bcrypt.checkpw')
    def test_is_admin_success(self, mock_checkpw, mock_admin_details):
        auth = Authentication()
        mock_admin_details.return_value = [['aman', 'password', b'password']]
        mock_checkpw.return_value = True

        result = auth.check_if_admin_exists('testuser', 'correctpassword')
        self.assertTrue(result)

    @patch('Business_Layer.authentication.utils.get_admin_details_from_username')
    @patch('bcrypt.checkpw')
    def test_is_admin_Failure(self, mock_checkpw, mock_admin_details):
        auth = Authentication()
        mock_admin_details.return_value = [['aman', 'password', b'password']]
        mock_checkpw.return_value = False

        result = auth.check_if_admin_exists('testuser', 'correctpassword')
        self.assertFalse(result)

    @patch('Business_Layer.authentication.utils.get_admin_details_from_username')
    def test_username_does_not_exist(self, mock_admin_details):
        #starting returning false
        auth = Authentication()
        mock_admin_details.return_value = []

        result = auth.check_if_admin_exists('testuser', 'correctpassword')
        self.assertFalse(result)

    # @patch('Database_Layer.db_utils.get_hashed_password')
    # @patch('bcrypt.checkpw')
    # def test_is_admin_failure(self, mock_checkpw, mock_get_hashed_password):
    #     auth = Authentication()
    #     mock_get_hashed_password.return_value = b'$2b$12$eix6Mh.6.O1M4fTzT5O1heQ6V.b0U8z6WnR8qxK8B/ywWjRvvMyQK'  # Example hashed password
    #     mock_checkpw.return_value = False
    #
    #     result = auth.is_admin('testuser', 'wrongpassword')
    #
    #     self.assertFalse(result)

    #doubt...... about encode
    @patch('Business_Layer.authentication.utils.get_admin_details_from_username')
    @patch('Business_Layer.authentication.bcrypt.checkpw')
    def test_is_admin_failure(self, mock_checkpw, mock_admin_details):

        #login successful == false

        username = 'testuser'
        password = 'wrongpassword'
        auth = Authentication()
        mock_admin_details.return_value = [('1', 'testuser', b'password')]
        mock_checkpw.return_value = False
        result=auth.check_if_admin_exists(username, password)
        mock_admin_details.assert_called_once_with(username)
        orignl_hash_pw = b'wrongpassword'
        mock_checkpw.assert_called_once_with(orignl_hash_pw, b'password')
        self.assertFalse(result)

    @patch('Business_Layer.authentication.utils.get_admin_details_from_username', return_value=True)
    @patch('Business_Layer.authentication.bcrypt.checkpw')
    def test_is_admin_failure_to_success(self, mock_checkpw, mock_admin_details):
        username = 'testuser'
        password = 'wrongpassword'
        auth = Authentication()
        mock_admin_details.return_value = [('1', 'testuser', b'password')]
        mock_checkpw.return_value = True
        result= auth.check_if_admin_exists(username, password)
        mock_admin_details.assert_called_once_with(username)
        orignl_hash_pw = b'wrongpassword'
        mock_checkpw.assert_called_once_with(b'wrongpassword', b'password')
        self.assertTrue(result)

    @patch('Database_Layer.db_utils.duplicate_usernames')
    def test_is_unique_username_success(self, mock_duplicate_usernames):
        auth = Authentication()
        mock_duplicate_usernames.return_value = []
        result = auth.is_unique_username('new_username')

        self.assertEqual(result, 1)
        mock_duplicate_usernames.assert_called_once_with('new_username')

    @patch('Database_Layer.db_utils.duplicate_usernames')
    def test_is_unique_username_failure(self, mock_duplicate_usernames):
        auth = Authentication()
        mock_duplicate_usernames.return_value = ['existing_user']

        result = auth.is_unique_username('existing_user')

        self.assertEqual(result, 0)
        mock_duplicate_usernames.assert_called_once_with('existing_user')

    @patch('Database_Layer.db_utils.insert_new_admin')
    def test_signup_new_admin(self, mock_insert_new_admin):
        auth = Authentication()
        auth.signup_new_admin('new_admin', 'new_password')

        mock_insert_new_admin.assert_called_once_with('new_admin', 'new_password')
