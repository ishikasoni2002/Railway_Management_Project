import unittest
import Business_Layer.Validations as validation
class TestCheckUsernameAndPasswordFormat(unittest.TestCase):
    def test_valid_usernames(self):
        self.assertTrue(validation.check_username_and_password_format('username', 'User1'))
        self.assertTrue(validation.check_username_and_password_format('username', 'A1b2C3d'))

    def test_invalid_usernames(self):
        self.assertFalse(validation.check_username_and_password_format('username', 'user'))
        self.assertFalse(validation.check_username_and_password_format('username', 'USER123'))
        self.assertFalse(validation.check_username_and_password_format('username', 'user123'))
        self.assertFalse(validation.check_username_and_password_format('username', 'User 123'))

    def test_valid_passwords(self):
        self.assertTrue(validation.check_username_and_password_format('password', 'Passw0rd!'))
        self.assertTrue(validation.check_username_and_password_format('password', 'P@ssw0rd!'))

    def test_invalid_passwords(self):
        self.assertFalse(validation.check_username_and_password_format('password', 'Password1'))
        self.assertFalse(validation.check_username_and_password_format('password', 'passw0rd!'))
        self.assertFalse(validation.check_username_and_password_format('password', 'PASSWORD!'))
        self.assertFalse(validation.check_username_and_password_format('password', 'Pass 123!'))
        self.assertFalse(validation.check_username_and_password_format('password', 'short!1'))
