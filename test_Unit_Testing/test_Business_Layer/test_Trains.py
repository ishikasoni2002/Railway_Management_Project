import unittest
from unittest.mock import patch

import Business_Layer.helper
import Database_Layer.db_utils
from Business_Layer.trains import Train
import json


class test_trains(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.train_obj = Train()
    @patch('Database_Layer.db_utils.show_all_trains')
    def test_show_all_trains_exist(self, mock_show_all_train):
        train = Train()
        mock_show_all_train.return_value = [(12345, 'SudhaExpress'), (12222,'Sabarmati_Exp')]
        train.show_all_trains()
        mock_show_all_train.assert_called_once()

    @patch('Database_Layer.db_utils.show_all_trains')
    def test_show_all_trains_not_exist(self, mock_show_all_train):
        train = Train()
        mock_show_all_train.return_value = []
        train.show_all_trains()
        mock_show_all_train.assert_called_once()


    @patch('Database_Layer.db_utils.get_train_details')
    def test_search_by_train_number_not_exist(self,mocked_train_details):

        mocked_train_details.return_value= None
        self.train_obj.search_by_train_number(12222)
        mocked_train_details.assert_called_once_with(12222)

    @patch('Business_Layer.helper.print_train_details')
    @patch('Database_Layer.db_utils.get_train_details')
    def test_search_by_train_number_exist(self, mocked_train_details,mocked_print_train_details):
        mocked_train_details.return_value = [(12222,'SFExpress')]
        mocked_print_train_details.return_value = [(12222,'SFExpress')]
        self.train_obj.search_by_train_number(12222)
        mocked_train_details.assert_called_once_with(12222)

    @patch('Business_Layer.helper.print_train_details')
    @patch('Database_Layer.db_utils.get_train_details_using_name')
    def test_search_by_train_name_exist(self, mocked_train_details, mocked_print_train_details):
        mocked_train_details.return_value = [(12222, 'SFExpress')]
        mocked_print_train_details.return_value = [(12222, 'SFExpress')]
        self.train_obj.search_by_train_name('SFExpress')
        mocked_train_details.assert_called_once_with('SFExpress')

    @patch('Database_Layer.db_utils.get_train_details_using_name')
    def test_search_by_train_name_not_exist(self, mocked_train_details):
        mocked_train_details.return_value = []
        self.train_obj.search_by_train_name('SFExpress')
        mocked_train_details.assert_called_once_with('SFExpress')

    @patch('Database_Layer.db_utils.get_route_details')
    @patch('Database_Layer.db_utils.get_train_details')
    @patch('Business_Layer.helper.convert_minutes_to_time')
    @patch('builtins.print')
    def test_show_route(self, mocked_print, mocked_convert_minutes_to_time, mocked_get_train_details,
                        mocked_get_route_details):
        mocked_get_train_details.return_value = ('123', 'Express 1')
        mocked_get_route_details.return_value = (
            json.dumps(["Station 1", "Station 2"]),
            json.dumps(["1", "2"]),
            json.dumps(["60", "120"])
        )
        mocked_convert_minutes_to_time.side_effect = ['01:00', '02:00']
        self.train_obj.show_route(123)

        mocked_print.assert_any_call('The Route of the Train 123 is as follows: ')
        mocked_print.assert_any_call('The train will arrive on Station 1 at platform 01 at 01:00')
        mocked_print.assert_any_call('The train will arrive on Station 2 at platform 02 at 02:00')

    @patch('Database_Layer.db_utils.get_route_details')
    @patch('Database_Layer.db_utils.get_train_details')
    @patch('Business_Layer.helper.json_string_to_list')
    @patch('builtins.print')
    def test_show_platform_number(self, mocked_print, mocked_json_string_to_list, mocked_get_train_details,
                                  mocked_get_route_details):
        mocked_get_train_details.return_value = ('123', 'Express 1')
        mocked_get_route_details.return_value = (
            json.dumps(['Station 1', 'Station 2']),
            json.dumps(['1', '2']),
        )
        mocked_json_string_to_list.side_effect = [
            ['Station 1', 'Station 2'],
            ['1', '2']
        ]
        self.train_obj.show_platform_number('123', 'Station 1')

        mocked_print.assert_called_once_with('The platform for Station 1 of train number 123 is: ', '1')

    @patch('Database_Layer.db_utils.get_train_details')
    @patch('Database_Layer.db_utils.get_route_details')
    @patch('Business_Layer.helper.json_string_to_list')
    @patch('builtins.print')
    def test_check_fare(self, mocked_print, mocked_json_string_to_list, mocked_get_route_details,
                        mocked_get_train_details):
        mocked_get_train_details.return_value = [(123, 'Express 1', 500)]
        mocked_get_route_details.return_value = (
            json.dumps(['Station 1', 'Station 2', 'Station 3']),
        )
        mocked_json_string_to_list.return_value = ['Station 1', 'Station 2', 'Station 3']

        self.train_obj.check_fare(123, 'Station 1', 'Station 3')

        mocked_print.assert_called_once_with(500.0)

    @patch('Database_Layer.db_utils.get_all_route_details')
    def test_show_train_using_stations(self, mocked_get_all_route_details):
        mocked_get_all_route_details.return_value = [
            (123, json.dumps(['Station 1', 'Station 2', 'Station 3'])),
            (456, json.dumps(['Station 2', 'Station 3', 'Station 4']))
        ]
        result = self.train_obj.show_train_using_stations('Station 1', 'Station 3')
        self.assertEqual(result, [123])




