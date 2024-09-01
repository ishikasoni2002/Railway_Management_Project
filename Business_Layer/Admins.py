import Database_Layer.db_utils as utils
import Business_Layer.Helper as helper


class Admin:

    def add_new_train(self, train_details):
        start_time_in_minutes = train_details['starting_station_time']
        end_time_in_minutes = train_details['ending_station_time']
        data_of_route = [train_details['list_of_stations'], train_details['list_of_platforms'],
                         train_details['list_of_arrival_time'], train_details['list_of_departure_time']]
        flag = helper.check_train_clash(start_time_in_minutes, end_time_in_minutes, data_of_route)

        if flag:
            print('There is a clashing with another Train! ')
        else:
            utils.insert_train_data(train_details)

    def remove_train(self, train_number):
        utils.delete_train(train_number)

    def update_train_fare(self, train_number,new_fare):
        utils.update_train_fare(train_number, new_fare)

    def update_train_platform(self, train_number, station, platform):
        pass

    def update_tc_assigned(self, train_number, new_tc):
        utils.update_tc_assigned(train_number,new_tc)

