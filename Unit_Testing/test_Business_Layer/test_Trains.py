import unittest
from unittest.mock import patch
from Business_Layer.Trains import Train


class test_trains(unittest.TestCase):

    @patch('Database_Layer.db_utils.show_all_trains')
    def test_show_all_trains(self, mock_show_all_train):
        train = Train()
        train.show_all_trains()
        mock_show_all_train.return_value = [(12345, 'SudhaExpress', 1000, 'Ramlal', 200, 500)]
        mock_show_all_train.assert_called_once()

    def test_search_by_train_number(self):
        pass

    @patch('Database_Layer.db_utils.get_route_details')
    @patch('Database_Layer.db_utils.get_train_details', return_value=True)
    def test_show_route_passed(self, mock_get_train_details, mock_get_route_details):
        train = Train()
        train_no = 12345
        train.show_route(train_no)
        mock_get_train_details.assert_called_once_with(12345)
        mock_get_route_details.assert_called_once_with(12345)

    @patch('Database_Layer.db_utils.get_route_details')
    @patch('Database_Layer.db_utils.get_train_details', return_value=False)
    def test_show_route_failed(self, mock_get_train_details, mock_get_route_details):
        train = Train()
        train_no = 12345
        train.show_route(train_no)
        mock_get_train_details.assert_called_once_with(12345)
        mock_get_route_details.assert_not_called()


    @patch('Database_Layer.db_utils.get_train_details')
    def test_show_platform_number(self):
        pass


    @patch('json.loads', return_value = ["Wwe", "Ener"])
    @patch('Database_Layer.db_utils.get_route_details', return_value = [('["Wwe", "Ener"]', '[1, 2]')])
    @patch('Database_Layer.db_utils.get_train_details', return_value= [(98765, 'xyz', 1000, 'Piyush', 60, 0)])
    def test_check_fare(self, mock_get_train_details,
                        mock_get_route_details,mock_json_loads):
        train = Train()
        train_no = 98765
        from_station = 'Wwe'
        to_station = 'Ener'
        fare = train.check_fare(train_no, from_station, to_station)
        mock_get_train_details.assert_called_once_with(98765)
        mock_get_route_details.assert_called_once_with(98765)
        mock_json_loads.assert_called_once_with('["Wwe", "Ener"]')
        self.assertEqual( 1000.0, fare)





