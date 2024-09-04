import unittest
from unittest.mock import patch
from Business_Layer.admins import Admin


class test_admins(unittest.TestCase):

    def test_add_new_train(self):
        pass

    @patch('Database_Layer.db_utils.delete_train')
    def test_remove_train(self, mock_delete_train):
        train_no = 12345
        admin = Admin()
        admin.remove_train(train_no)
        mock_delete_train.assert_called_once_with(train_no)

    @patch('Database_Layer.db_utils.update_train_fare')
    def test_update_train_fare(self, mock_update_train_fare):
        admin = Admin()
        train_no = 12345
        new_fare = 4000
        admin.update_train_fare(train_no, new_fare)
        mock_update_train_fare.assert_called_once_with(train_no, new_fare)

    @patch('Database_Layer.db_utils.update_tc_assigned')
    def test_update_tc_assigned(self, mock_update_tc_assigned):
        admin = Admin()
        train_no = 12345
        new_tc = 'Raju'
        admin.update_tc_assigned(train_no, new_tc)
        mock_update_tc_assigned.assert_called_once_with(train_no, new_tc)
