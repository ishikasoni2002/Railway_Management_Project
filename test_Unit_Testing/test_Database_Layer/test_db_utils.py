import unittest
from unittest.mock import patch, MagicMock
from Database_Layer.connection import cur, conn
import Database_Layer.db_utils as db_utils
from Database_Layer.db_utils import cur,conn
import json

class TestDatabaseLayer(unittest.TestCase):

    @patch('Database_Layer.db_utils.cur')
    @patch('Database_Layer.db_utils.conn')
    def test_create_tables_if_not_exists(self, mock_conn, mock_cur):
        db_utils.create_tables_if_not_exists()
        # Check that the necessary SQL statements were executed
        self.assertEqual(mock_cur.execute.call_count, 4)
        mock_conn.commit.assert_called_once()

    @patch('Database_Layer.db_utils.cur')
    @patch('Database_Layer.db_utils.conn')
    def test_insert_new_admin(self, mock_conn, mock_cur):
        username = 'testuser'
        hashed_password = b'hashedpassword'
        db_utils.insert_new_admin(username, hashed_password)

        mock_cur.execute.assert_called_once()
        mock_conn.commit.assert_called_once()

    @patch('Database_Layer.db_utils.cur')
    def test_get_admin_users(self, mock_cur):
        mock_cur.execute.return_value.fetchall.return_value = [
            (1, 'admin1', 'hashedpassword1'),
            (2, 'admin2', 'hashedpassword2')
        ]

        result = db_utils.get_admin_users()
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], (1, 'admin1', 'hashedpassword1'))

    @patch('Database_Layer.db_utils.cur')
    def test_check_if_admin_table_empty(self, mock_cur):
        mock_cur.execute.return_value.fetchall.return_value = []

        result = db_utils.check_if_admin_table_empty()
        self.assertTrue(result)

    @patch('Database_Layer.db_utils.cur')
    @patch('Database_Layer.db_utils.conn')
    def test_insert_first_admin_into_AdminUsers(self, mock_conn, mock_cur):
        username = 'firstadmin'
        hashed_password = 'hashedpassword'
        mock_cur.execute.return_value.fetchall.return_value = []

        db_utils.insert_first_admin_into_AdminUsers(username, hashed_password)
        mock_cur.execute.assert_called_with('INSERT INTO AdminUsers VALUES(null, ?, ?)',
                                                 (username, hashed_password))
        mock_conn.commit.assert_called()

    @patch('Database_Layer.db_utils.cur')
    def test_get_admin_details_from_username(self, mock_cur):
        username = 'testuser'
        mock_cur.execute.return_value.fetchall.return_value = [
            (1, 'testuser', 'hashedpassword')
        ]

        result = db_utils.get_admin_details_from_username(username)
        self.assertEqual(result[0][1], username)

    @patch('Database_Layer.db_utils.cur')
    @patch('Database_Layer.db_utils.conn')
    def test_delete_admin(self, mock_conn, mock_cur):
        username = 'testuser'

        db_utils.delete_admin(username)
        mock_cur.execute.assert_called_with('DELETE FROM AdminUsers WHERE USERNAMES = ?', (username,))
        mock_conn.commit.assert_called_once()

    @patch('Database_Layer.db_utils.cur')
    def test_get_hashed_password(self, mock_cur):
        username = 'testuser'
        mock_cur.execute.return_value.fetchall.return_value = [
            ('hashedpassword',)
        ]

        result = db_utils.get_hashed_password(username)
        self.assertEqual(result, 'hashedpassword')

    @patch('Database_Layer.db_utils.cur')
    def test_duplicate_usernames(self, mock_cur):
        username = 'testuser'
        mock_cur.execute.return_value.fetchall.return_value = [
            (1, 'testuser', 'hashedpassword')
        ]

        result = db_utils.duplicate_usernames(username)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][1], username)

    @patch('Database_Layer.db_utils.cur')
    def test_show_all_trains(self, mock_cur):
        mock_cur.execute.return_value.fetchall.return_value = [
            (123, 'Express 1', 500, 'TC1', 600, 1200),
            (456, 'Express 2', 300, 'TC2', 800, 1400)
        ]

        result = db_utils.show_all_trains()
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0][1], 'Express 1')

    @patch('Database_Layer.db_utils.cur')
    def test_get_train_details(self, mock_cur):
        train_number = 123
        mock_cur.execute.return_value.fetchall.return_value = [
            (123, 'Express 1', 500, 'TC1', 600, 1200)
        ]

        result = db_utils.get_train_details(train_number)
        self.assertEqual(result[0][0], train_number)

    @patch('Database_Layer.db_utils.cur')
    def test_get_train_details_using_name(self, mock_cur):
        train_name = 'Express 1'
        mock_cur.execute.return_value.fetchall.return_value = [
            (123, train_name, 500, 'TC1', 600, 1200)
        ]

        result = db_utils.get_train_details_using_name(train_name)
        self.assertEqual(result[0][1], train_name)

    @patch('Database_Layer.db_utils.cur')
    @patch('Database_Layer.db_utils.conn')
    def test_delete_train(self, mock_conn, mock_cur):
        train_number = 123

        db_utils.delete_train(train_number)
        mock_cur.execute.assert_any_call('DELETE FROM Trains WHERE TRAIN_NUMBER =?', (train_number,))
        mock_cur.execute.assert_any_call('DELETE FROM Train_Route WHERE TRAIN_NUMBER =?', (train_number,))
        mock_conn.commit.assert_called_once()

    @patch('Database_Layer.db_utils.cur')
    def test_get_all_route_details(self, mock_cur):
        mock_cur.execute.return_value.fetchall.return_value = [
            (123, '{"Station 1", "Station 2"}', '[1, 2]', '[60, 120]', '[75, 135]')
        ]

        result = db_utils.get_all_route_details()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0], 123)

    @patch('Database_Layer.db_utils.cur')
    def test_get_route_details(self, mock_cur):
        train_number = 123
        mock_cur.execute.return_value.fetchone.return_value = (
            '{"Station 1", "Station 2"}', '[1, 2]', '[60, 120]'
        )

        result = db_utils.get_route_details(train_number)
        self.assertEqual(result[0], '{"Station 1", "Station 2"}')

    @patch('Database_Layer.db_utils.cur')
    @patch('Database_Layer.db_utils.conn')
    def test_insert_train_data(self, mock_conn, mock_cur):
        train_details = {
            'train_no': 123,
            'train_name': 'Express 1',
            'train_fare': 500,
            'tc_assigned': 'TC1',
            'starting_station_time': 600,
            'ending_station_time': 1200,
            'route': ['Station 1', 'Station 2'],
            'platform_number': [1, 2],
            'arrival_time': [60, 120],
            'departure_time': [75, 135]
        }

        db_utils.insert_train_data(train_details)

        mock_cur.execute.assert_any_call(
            'INSERT INTO Trains VALUES(?,?,?,?,?,?)',
            (123, 'Express 1', 500, 'TC1', 600, 1200)
        )
        mock_cur.execute.assert_any_call(
            'INSERT INTO Train_Route VALUES(?,?,?,?,?)',
            (123, json.dumps(['Station 1', 'Station 2']), json.dumps([1, 2]), json.dumps([60, 120]),
             json.dumps([75, 135]))
        )
        mock_conn.commit.assert_called_once()

    @patch('Database_Layer.db_utils.cur')
    @patch('Database_Layer.db_utils.conn')
    def test_update_train_fare(self, mock_conn, mock_cur):
        train_no = 123
        new_fare = 600

        db_utils.update_train_fare(new_fare, train_no)
        mock_cur.execute.assert_called_once_with('UPDATE Trains SET TRAIN_FARE =? WHERE TRAIN_NUMBER = ?',
                                                 (new_fare, train_no))
        mock_conn.commit.assert_called_once()

    @patch('Database_Layer.db_utils.cur')
    @patch('Database_Layer.db_utils.conn')
    def test_update_tc_assigned(self, mock_conn, mock_cur):
        train_number = 123
        new_tc = 'New TC'
        mock_cur.execute.return_value.fetchall.return_value = [
            (123, 'Express 1', 500, 'TC1', 600, 1200)
        ]


