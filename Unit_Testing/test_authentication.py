import unittest
from unittest.mock import patch
from Business_Layer.Authentication import authentication


auth = authentication()

class testAuthentication(unittest.TestCase):
    @patch('Database_Layer.db_utils.create_tables_if_not_exists')
    def test_initiate_all_tables(self, mock_create_tables):
        auth.initiate_all_tables()
        mock_create_tables.assert_called_once()

    def test_check_root_password(self):
        self.assertFalse(auth.check_root_password('Ishika23'),'Ishika@123')
        self.assertTrue(auth.check_root_password('Ishika@123'), 'Ishika@123')

    @patch('Database_Layer.db_utils.get_hashed_password')
    @patch('bcrypt.checkpw')
    def test_is_admin_success(self, mock_checkpw, mock_get_hashed_password):
        mock_get_hashed_password.return_value = b'$2b$12$eix6Mh.6.O1M4fTzT5O1heQ6V.b0U8z6WnR8qxK8B/ywWjRvvMyQK'  # Example hashed password
        mock_checkpw.return_value = True

        result = auth.is_admin('testuser', 'correctpassword')

        self.assertTrue(result)

    @patch('Database_Layer.db_utils.get_hashed_password')
    @patch('bcrypt.checkpw')
    def test_is_admin_failure(self, mock_checkpw, mock_get_hashed_password):

        mock_get_hashed_password.return_value = b'$2b$12$eix6Mh.6.O1M4fTzT5O1heQ6V.b0U8z6WnR8qxK8B/ywWjRvvMyQK'  # Example hashed password
        mock_checkpw.return_value = False

        result = auth.is_admin('testuser', 'wrongpassword')

        self.assertFalse(result)

    @patch('Database_Layer.db_utils.duplicate_usernames')
    def test_is_unique_username_success(self, mock_duplicate_usernames):
        mock_duplicate_usernames.return_value = []
        result = auth.is_unique_username('newusername')

        self.assertEqual(result, 1)

    @patch('Database_Layer.db_utils.duplicate_usernames')
    def test_is_unique_username_failure(self, mock_duplicate_usernames):
        mock_duplicate_usernames.return_value = ['existinguser']

        result = auth.is_unique_username('existinguser')

        self.assertEqual(result, 1)
        mock_duplicate_usernames.assert_called_once_with('existinguser')

    @patch('Database_Layer.db_utils.insert_new_admin')
    def test_signup_new_admin(self, mock_insert_new_admin):
        auth.signup_new_admin('newadmin', 'newpassword')

        mock_insert_new_admin.assert_called_once_with('newadmin', 'newpassword')