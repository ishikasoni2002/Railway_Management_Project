import unittest
from unittest.mock import patch
import Business_Layer.validations


class TestValidationFunctions(unittest.TestCase):

    def test_check_username_and_password_format_username(self):
        self.assertTrue(Business_Layer.validations.check_username_and_password_format('username', 'User1A'))
        self.assertFalse(Business_Layer.validations.check_username_and_password_format('username', 'user1'))
        self.assertFalse(Business_Layer.validations.check_username_and_password_format('username', 'USER1'))
        self.assertFalse(Business_Layer.validations.check_username_and_password_format('username', 'User1!'))

    def test_check_username_and_password_format_password(self):
        self.assertTrue(Business_Layer.validations.check_username_and_password_format('password', 'Password1!'))
        self.assertFalse(Business_Layer.validations.check_username_and_password_format('password', 'password'))
        self.assertFalse(Business_Layer.validations.check_username_and_password_format('password', 'PASSWORD123'))
        self.assertFalse(Business_Layer.validations.check_username_and_password_format('password', 'Pass1 word'))
        self.assertFalse(Business_Layer.validations.check_username_and_password_format('password', 'P@ss1'))

    def test_check_time_format(self):
        self.assertTrue(Business_Layer.validations.check_time_format('00:00'))
        self.assertTrue(Business_Layer.validations.check_time_format('23:59'))
        self.assertFalse(Business_Layer.validations.check_time_format('24:00'))
        self.assertFalse(Business_Layer.validations.check_time_format('12:60'))
        self.assertFalse(Business_Layer.validations.check_time_format('12:5'))
        self.assertFalse(Business_Layer.validations.check_time_format('abc:def'))

    def test_check_train_number_format(self):
        self.assertTrue(Business_Layer.validations.check_train_number_format('12345'))
        self.assertFalse(Business_Layer.validations.check_train_number_format('1234'))
        self.assertFalse(Business_Layer.validations.check_train_number_format('123456'))
        self.assertFalse(Business_Layer.validations.check_train_number_format('12abc'))

    def test_check_station_name_format(self):
        self.assertTrue(Business_Layer.validations.check_station_name_format('Station'))
        self.assertFalse(Business_Layer.validations.check_station_name_format('Station123'))
        self.assertFalse(Business_Layer.validations.check_station_name_format('Station!'))
        self.assertFalse(Business_Layer.validations.check_station_name_format('Station Name'))


if __name__ == '__main__':
    unittest.main()
