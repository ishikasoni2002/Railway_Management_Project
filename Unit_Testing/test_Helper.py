import unittest
from unittest.mock import patch, MagicMock
import json
import Business_Layer.Helper

class TestCheckTrainClash(unittest.TestCase):

    @patch('Database_Layer.db_utils.get_time_details_of_start_and_end')
    @patch('Database_Layer.db_utils.get_all_route_details')
    def test_check_train_clash_success(self, mock_get_all_route_details, mock_get_time_details):
        mock_get_time_details.return_value = [
            ('some_value', 10, 20)
        ]
        mock_get_all_route_details.return_value = [
            (1, json.dumps(['StationA', 'StationB']), json.dumps(['Platform1', 'Platform2']), json.dumps([10, 20])),
            (2, json.dumps(['StationX', 'StationY']), json.dumps(['Platform3', 'Platform4']), json.dumps([30, 40]))
        ]

        start_time_in_minutes = 5
        end_time_in_minutes = 25
        data_of_route = (
            ['StationA', 'StationB'],
            ['Platform1', 'Platform2'],
            [10, 20],
            [5, 15]
        )

        result = Business_Layer.Helper.check_train_clash(start_time_in_minutes, end_time_in_minutes, data_of_route)
        self.assertTrue(result)

    @patch('Database_Layer.db_utils.get_time_details_of_start_and_end')
    @patch('Database_Layer.db_utils.get_all_route_details')
    def test_check_train_clash_no_clash(self, mock_get_all_route_details, mock_get_time_details):

        mock_get_time_details.return_value = [
            ('some_value', 10, 20)
        ]
        mock_get_all_route_details.return_value = [
            (1, json.dumps(['StationA', 'StationB']), json.dumps(['Platform1', 'Platform2']), json.dumps([30, 40])),
            (2, json.dumps(['StationX', 'StationY']), json.dumps(['Platform3', 'Platform4']), json.dumps([50, 60]))
        ]

        start_time_in_minutes = 5
        end_time_in_minutes = 15
        data_of_route = (
            ['StationA', 'StationB'],
            ['Platform1', 'Platform2'],
            [10, 20],
            [5, 15]
        )

        result = Business_Layer.Helper.check_train_clash(start_time_in_minutes, end_time_in_minutes, data_of_route)
        self.assertFalse(result)


