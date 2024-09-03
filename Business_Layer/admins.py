import json

import Database_Layer.db_utils as utils
import Business_Layer.helper as helper


class Admin:

    def add_new_train(self, train_details):
        if utils.get_train_details(train_details['train_no']):
            print('Train Number already exists! ')
            return
        start_time_in_minutes = train_details['starting_station_time']
        end_time_in_minutes = train_details['ending_station_time']
        data_of_route = [train_details['route'], train_details['platform_number'],
                         train_details['arrival_time'], train_details['departure_time']]
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
        train_details = utils.get_route_details(train_number)
        route_details= json.loads(train_details[0][0]) #list
        platform_details= json.loads(train_details[0][1]) #list
        print(route_details,train_details,platform_details)

        for index in range(len(route_details)):
            if route_details[index] == station:
                platform_details[index] = platform
                print(platform_details[index])
                platform_details = json.dumps(platform_details)
                print(platform_details,type(platform_details))
                utils.update_station_platform(train_number, platform_details)
                break


    def update_tc_assigned(self, train_number, new_tc):
        utils.update_tc_assigned(train_number,new_tc)

