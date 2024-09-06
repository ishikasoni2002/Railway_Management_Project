import unittest
from unittest.mock import patch
from Business_Layer.admins import Admin


class test_admins(unittest.TestCase):



    @patch('Business_Layer.admins.utils.get_train_details', return_value =True)
    def test_add_new_train_success_getTrainDetails(self, mock_get_train_details):
        train_details = {
        'train_no': 12345, 'train_name': 'Ishika', 'train_fare': 1000,
        'tc_assigned': 'Raju', 'starting_station_time': 600,
        'ending_station_time': 800, 'route': ["sog","bkn"],
        'platform_number': [1,2],'arrival_time': [600,800],
        'departure_time': [610,810]
        }

        admin = Admin()
        admin.add_new_train(train_details)
        mock_get_train_details.assert_called_once_with(train_details['train_no'])



    @patch('Business_Layer.admins.helper.check_train_clash', return_value = True)
    @patch('Business_Layer.admins.utils.get_train_details', return_value=False)
    def test_add_new_train_Failure_getTrainDetails_flagTrue(self, mock_get_train_details, mock_check_train_clash):
        train_details = {
            'train_no': 12345, 'train_name': 'Ishika', 'train_fare': 1000,
            'tc_assigned': 'Raju', 'starting_station_time': 600,
            'ending_station_time': 800, 'route': ["sog", "bkn"],
            'platform_number': [1, 2], 'arrival_time': [600, 800],
            'departure_time': [610, 810]
        }

        admin = Admin()
        admin.add_new_train(train_details)
        mock_get_train_details.assert_called_once_with(train_details['train_no'])
        start_time_in_minutes = train_details['starting_station_time']
        end_time_in_minutes = train_details['ending_station_time']
        data_of_route = [train_details['route'], train_details['platform_number'],
                         train_details['arrival_time'], train_details['departure_time']]

        mock_check_train_clash.assert_called_once_with(start_time_in_minutes,end_time_in_minutes,data_of_route)

    @patch('Business_Layer.admins.helper.check_train_clash', return_value=False)
    @patch('Business_Layer.admins.utils.get_train_details', return_value=False)
    def test_add_new_train_Failure_getTrainDetails_flagFalse_time(self, mock_get_train_details, mock_check_train_clash):

        #start time greater than end time
        train_details = {
            'train_no': 12345, 'train_name': 'Ishika', 'train_fare': 1000,
            'tc_assigned': 'Raju', 'starting_station_time': 800,
            'ending_station_time': 600, 'route': ["sog", "bkn"],
            'platform_number': [1, 2], 'arrival_time': [800, 600],
            'departure_time': [810, 610]
        }

        admin = Admin()
        admin.add_new_train(train_details)
        mock_get_train_details.assert_called_once_with(train_details['train_no'])
        start_time_in_minutes = train_details['starting_station_time']
        end_time_in_minutes = train_details['ending_station_time']
        data_of_route = [train_details['route'], train_details['platform_number'],
                         train_details['arrival_time'], train_details['departure_time']]

        mock_check_train_clash.assert_called_once_with(start_time_in_minutes, end_time_in_minutes, data_of_route)



    @patch('Business_Layer.admins.helper.check_train_clash', return_value=False)
    @patch('Business_Layer.admins.utils.get_train_details', return_value=False)
    def test_add_new_train_Failure_getTrainDetails_flagFalse_more_than_12_hr(self, mock_get_train_details, mock_check_train_clash):

        #more than 12 hr journey
        train_details = {
            'train_no': 12345, 'train_name': 'Ishika', 'train_fare': 1000,
            'tc_assigned': 'Raju', 'starting_station_time': 00,
            'ending_station_time': 800, 'route': ["sog", "bkn"],
            'platform_number': [1, 2], 'arrival_time': [00, 800],
            'departure_time': [10, 810]
        }

        admin = Admin()
        admin.add_new_train(train_details)
        mock_get_train_details.assert_called_once_with(train_details['train_no'])
        start_time_in_minutes = train_details['starting_station_time']
        end_time_in_minutes = train_details['ending_station_time']
        data_of_route = [train_details['route'], train_details['platform_number'],
                         train_details['arrival_time'], train_details['departure_time']]

        mock_check_train_clash.assert_called_once_with(start_time_in_minutes, end_time_in_minutes, data_of_route)


    @patch('Business_Layer.admins.utils.insert_train_data')
    @patch('Business_Layer.admins.helper.check_train_clash', return_value=False)
    @patch('Business_Layer.admins.utils.get_train_details', return_value=False)
    def test_add_new_train_Failure_getTrainDetails_flagFalse_insertData(self, mock_get_train_details,
                                                                             mock_check_train_clash, mock_insert_trainData):
        # insert Train data
        train_details = {
            'train_no': 12345, 'train_name': 'Ishika', 'train_fare': 1000,
            'tc_assigned': 'Raju', 'starting_station_time': 600,
            'ending_station_time': 800, 'route': ["sog", "bkn"],
            'platform_number': [1, 2], 'arrival_time': [600, 800],
            'departure_time': [610, 810]
        }

        admin = Admin()
        admin.add_new_train(train_details)
        mock_get_train_details.assert_called_once_with(train_details['train_no'])
        start_time_in_minutes = train_details['starting_station_time']
        end_time_in_minutes = train_details['ending_station_time']
        data_of_route = [train_details['route'], train_details['platform_number'],
                         train_details['arrival_time'], train_details['departure_time']]

        mock_insert_trainData.assert_called_once_with(train_details)



    @patch('Database_Layer.db_utils.delete_train')
    def test_remove_train(self, mock_delete_train):
        train_no = 12345
        admin = Admin()
        admin.remove_train(train_no)
        mock_delete_train.assert_called_once_with(train_no)

    @patch('Business_Layer.admins.utils.get_train_details', return_value = [])
    def test_update_train_fare_Failure(self, mock_update_train_fare):
        admin = Admin()
        train_no = 12345
        new_fare = 4000
        admin.update_train_fare(train_no, new_fare)
        mock_update_train_fare.assert_called_once_with(train_no)

    @patch('Business_Layer.admins.utils.update_train_fare')
    @patch('Business_Layer.admins.utils.get_train_details', return_value=[('12345, "Ishika", 400, "Raju" , 500, 600')])
    def test_update_train_fare_Success(self, mock_update_train_fare, mock_train_fare):
        admin = Admin()
        train_no = 12345
        new_fare = 4000
        admin.update_train_fare(train_no, new_fare)
        mock_update_train_fare.assert_called_once_with(train_no)
        mock_train_fare.assert_called_once_with(new_fare,train_no)



    @patch('Business_Layer.admins.utils.get_train_details', return_value =False)
    def test_update_train_platform_success_train_details(self, mock_train_details):
        #only when no data is present about a particular train

        train_no = 12345
        station = 'suratgarh'
        platform = 1

        admin = Admin()
        admin.update_train_platform(train_no, station, platform)

        mock_train_details.assert_called_once_with(train_no)

    @patch('Business_Layer.admins.utils.get_train_details', return_value=False)
    def test_update_train_platform_success_train_details(self, mock_train_details):
        # only when no data is present about a particular train

        train_no = 12345
        station = 'suratgarh'
        platform = 1

        admin = Admin()
        admin.update_train_platform(train_no, station, platform)

        mock_train_details.assert_called_once_with(train_no)





    @patch('Database_Layer.db_utils.update_tc_assigned')
    def test_update_tc_assigned(self, mock_update_tc_assigned):
        admin = Admin()
        train_no = 12345
        new_tc = 'Raju'
        admin.update_tc_assigned(train_no, new_tc)
        mock_update_tc_assigned.assert_called_once_with(train_no, new_tc)
