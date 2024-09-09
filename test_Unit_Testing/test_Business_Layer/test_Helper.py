import unittest
from unittest.mock import patch, MagicMock
import json
import Business_Layer.helper

class TestCheckTrainClash(unittest.TestCase):

    @patch('Business_Layer.helper.utils.get_time_details_of_start_and_end')
    @patch('Business_Layer.helper.utils.get_all_route_details')
    def test_check_train_clash(self, mock_get_all_route_details, mock_get_time_details_of_start_and_end):
        # Mock data
        mock_get_time_details_of_start_and_end.return_value = [
            (12222, 600, 900),  # Train 1: 10:00 AM - 3:00 PM
            (12223, 930, 1200),  # Train 2: 9:30 AM - 8:00 PM
        ]

        mock_get_all_route_details.return_value = [
            (12222, json.dumps(['Station A', 'Station B', 'Station C']),
             json.dumps([1, 2, 3]), json.dumps([600, 700, 800])),
            (12223, json.dumps(['Station A', 'Station B', 'Station C']),
             json.dumps([1, 2, 3]), json.dumps([930, 1030, 1130]))
        ]

        train_route = ['Station A', 'Station B', 'Station C']
        platforms = [1, 2, 3]
        arrival_times = [630, 730, 830]  # Overlaps with Train 1

        data_of_route = (train_route, platforms, arrival_times, arrival_times)

        result = Business_Layer.helper.check_train_clash(615, 850, data_of_route)
        # self.assertTrue(result)
        train_route = ['Station D', 'Station E', 'Station F']
        platforms = [1, 2, 3]
        arrival_times = [1000, 1100, 1200]

        data_of_route = (train_route, platforms, arrival_times, arrival_times)

        result = Business_Layer.helper.check_train_clash(850, 1200, data_of_route)
        self.assertFalse(result)

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

        result = Business_Layer.helper.check_train_clash(start_time_in_minutes, end_time_in_minutes, data_of_route)
        self.assertFalse(result)


